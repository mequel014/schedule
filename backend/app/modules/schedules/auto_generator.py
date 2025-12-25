# ./app/modules/schedules/auto_generator.py

from sqlmodel import Session
from typing import List, Dict, Set
from uuid import UUID
from datetime import date, time
import calendar
import random

from .models import Schedule
from .utils import get_default_shift_times, is_weekend_or_holiday, get_preferences_for_month
from app.modules.shifts.models import Shift
from app.modules.doctors.utils import get_all_doctors, get_doctor_profile
from app.modules.preferences.models import DayPreference


def generate_schedule(
    session: Session,
    schedule: Schedule,
    seed: int = None
) -> List[Shift]:
    """
    Auto-generate schedule based on:
    1. Doctor preferences
    2. Minimum shifts per doctor
    3. Priority (higher = more likely to get contested days)
    4. No consecutive days for same doctor
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    
    year = schedule.year
    month = schedule.month
    
    # Get all days in month
    num_days = calendar.monthrange(year, month)[1]
    all_days = [date(year, month, d) for d in range(1, num_days + 1)]
    
    # Get doctors and their profiles
    doctors = get_all_doctors(session)
    doctor_data = {}
    for doc in doctors:
        profile = doc.doctor_profile
        if profile:
            doctor_data[doc.id] = {
                "user": doc,
                "priority": profile.priority,
                "min_shifts": profile.min_shifts_per_month,
                "assigned_count": 0,
                "last_shift_date": None
            }
    
    # Get preferences
    preferences = get_preferences_for_month(session, year, month)
    day_preferences: Dict[date, List[UUID]] = {}
    for pref in preferences:
        pref_date = date(year, month, pref.day)
        if pref_date not in day_preferences:
            day_preferences[pref_date] = []
        day_preferences[pref_date].append(pref.user_id)
    
    # Generate shifts
    generated_shifts: List[Shift] = []
    
    for day_date in all_days:
        start_time, end_time = get_default_shift_times(day_date, schedule)
        
        # Get doctors who want this day
        preferred_doctors = day_preferences.get(day_date, [])
        
        # Filter out doctors who worked yesterday
        available_preferred = [
            doc_id for doc_id in preferred_doctors
            if doc_id in doctor_data and
            doctor_data[doc_id]["last_shift_date"] != day_date - timedelta(days=1)
        ]
        
        selected_doctor_id = None
        
        if available_preferred:
            # Sort by priority (descending), then by assigned count (ascending)
            available_preferred.sort(
                key=lambda d: (
                    -doctor_data[d]["priority"],
                    doctor_data[d]["assigned_count"]
                )
            )
            selected_doctor_id = available_preferred[0]
        else:
            # No preferences - find doctor with lowest assignments who didn't work yesterday
            available_doctors = [
                doc_id for doc_id in doctor_data
                if doctor_data[doc_id]["last_shift_date"] != day_date - timedelta(days=1)
            ]
            
            if available_doctors:
                available_doctors.sort(
                    key=lambda d: (
                        doctor_data[d]["assigned_count"],
                        -doctor_data[d]["priority"]
                    )
                )
                selected_doctor_id = available_doctors[0]
        
        if selected_doctor_id:
            shift = Shift(
                schedule_id=schedule.id,
                doctor_id=selected_doctor_id,
                date=day_date,
                start_time=start_time,
                end_time=end_time
            )
            generated_shifts.append(shift)
            
            # Update doctor data
            doctor_data[selected_doctor_id]["assigned_count"] += 1
            doctor_data[selected_doctor_id]["last_shift_date"] = day_date
    
    return generated_shifts


def apply_generated_schedule(session: Session, schedule: Schedule, shifts: List[Shift]):
    """Remove existing shifts and apply new ones"""
    from sqlmodel import delete
    
    # Delete existing shifts
    statement = delete(Shift).where(Shift.schedule_id == schedule.id)
    session.exec(statement)
    
    # Add new shifts
    for shift in shifts:
        session.add(shift)
    
    session.commit()


from datetime import timedelta