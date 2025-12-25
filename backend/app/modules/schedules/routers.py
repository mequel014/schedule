# ./app/modules/schedules/routers.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import date, time
import calendar
import random

from app.core.db import get_session
from app.core.security import get_current_user, get_current_admin
from app.modules.users.models import User
from app.modules.users.enums import UserRole
from app.modules.shifts.models import Shift
from .models import Schedule, DayShiftSettings
from .schemas import (
    ScheduleCreate, ScheduleUpdate, ScheduleRead, ShiftCreate, ShiftUpdate, ShiftRead,
    DayShiftSettingsCreate, DayShiftSettingsRead, CalendarMonth, DayInfo
)
from . import utils
from .auto_generator import generate_schedule, apply_generated_schedule

router = APIRouter(prefix="/api/schedules", tags=["schedules"])


# ==========================================
# Schedule CRUD
# ==========================================

@router.get("", response_model=List[ScheduleRead])
async def list_schedules(
    year: int = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List schedules. Doctors only see visible/published ones."""
    statement = select(Schedule)
    if year:
        statement = statement.where(Schedule.year == year)
    
    # Filter for non-admin users
    if current_user.role == UserRole.DOCTOR:
        statement = statement.where(
            (Schedule.is_visible == True) | (Schedule.is_published == True)
        )
    
    schedules = session.exec(statement.order_by(Schedule.year.desc(), Schedule.month.desc())).all()
    
    result = []
    for schedule in schedules:
        shifts_data = []
        for shift in schedule.shifts:
            shift_read = ShiftRead.model_validate(shift)
            shift_read.doctor_name = shift.doctor.full_name if shift.doctor else None
            shifts_data.append(shift_read)
        
        schedule_read = ScheduleRead(
            id=schedule.id,
            year=schedule.year,
            month=schedule.month,
            is_visible=schedule.is_visible,
            is_published=schedule.is_published,
            shifts=shifts_data,
            day_settings=[DayShiftSettingsRead.model_validate(ds) for ds in schedule.day_settings]
        )
        result.append(schedule_read)
    
    return result


@router.get("/current", response_model=CalendarMonth)
async def get_current_schedule(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current month's schedule as calendar"""
    today = date.today()
    return await get_schedule_calendar(today.year, today.month, current_user, session)


@router.get("/next", response_model=CalendarMonth)
async def get_next_schedule(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get next month's schedule as calendar"""
    today = date.today()
    year = today.year
    month = today.month + 1
    if month > 12:
        month = 1
        year += 1
    return await get_schedule_calendar(year, month, current_user, session)


@router.get("/{year}/{month}", response_model=CalendarMonth)
async def get_schedule_calendar(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get schedule for specific month as calendar"""
    schedule = utils.get_schedule(session, year, month)
    
    # Check visibility for doctors
    if current_user.role == UserRole.DOCTOR:
        if schedule and not schedule.is_visible and not schedule.is_published:
            raise HTTPException(status_code=403, detail="Schedule not visible yet")
    
    num_days = calendar.monthrange(year, month)[1]
    
    # Get preferences for this month
    preferences = utils.get_preferences_for_month(session, year, month)
    pref_by_day = {}
    for pref in preferences:
        if pref.day not in pref_by_day:
            pref_by_day[pref.day] = []
        pref_by_day[pref.day].append(pref.user_id)
    
    days = []
    for d in range(1, num_days + 1):
        day_date = date(year, month, d)
        start_time, end_time = utils.get_default_shift_times(day_date, schedule)
        is_holiday = utils.is_weekend_or_holiday(day_date, schedule)
        
        # Get shifts for this day
        shifts_data = []
        if schedule:
            day_shifts = utils.get_shifts_for_day(session, schedule.id, day_date)
            for shift in day_shifts:
                shift_read = ShiftRead.model_validate(shift)
                shift_read.doctor_name = shift.doctor.full_name if shift.doctor else None
                shifts_data.append(shift_read)
        
        days.append(DayInfo(
            date=day_date,
            day_of_week=day_date.weekday(),
            is_weekend=day_date.weekday() >= 5,
            is_holiday=is_holiday and day_date.weekday() < 5,
            default_start_time=start_time,
            default_end_time=end_time,
            shifts=shifts_data,
            preferred_doctors=pref_by_day.get(d, [])
        ))
    
    return CalendarMonth(
        year=year,
        month=month,
        days=days,
        is_visible=schedule.is_visible if schedule else False,
        is_published=schedule.is_published if schedule else False
    )


@router.post("", response_model=ScheduleRead)
async def create_schedule(
    data: ScheduleCreate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Create or get schedule for month"""
    schedule = utils.get_or_create_schedule(session, data.year, data.month)
    return ScheduleRead.model_validate(schedule)


@router.patch("/{schedule_id}", response_model=ScheduleRead)
async def update_schedule(
    schedule_id: UUID,
    data: ScheduleUpdate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Update schedule visibility/published status"""
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(schedule, key, value)
    
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    
    return ScheduleRead.model_validate(schedule)


# ==========================================
# Auto-generate
# ==========================================

@router.post("/{year}/{month}/generate")
async def auto_generate_schedule(
    year: int,
    month: int,
    seed: int = Query(None, description="Random seed for reproducibility"),
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Auto-generate schedule for month"""
    schedule = utils.get_or_create_schedule(session, year, month)
    
    # Generate with random seed if not provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    shifts = generate_schedule(session, schedule, seed)
    apply_generated_schedule(session, schedule, shifts)
    
    # Refresh and return
    session.refresh(schedule)
    
    shifts_data = []
    for shift in schedule.shifts:
        shift_read = ShiftRead.model_validate(shift)
        shift_read.doctor_name = shift.doctor.full_name if shift.doctor else None
        shifts_data.append(shift_read)
    
    return {
        "schedule": ScheduleRead.model_validate(schedule),
        "shifts": shifts_data,
        "seed": seed
    }


# ==========================================
# Day Settings
# ==========================================

@router.post("/{schedule_id}/day-settings", response_model=DayShiftSettingsRead)
async def set_day_settings(
    schedule_id: UUID,
    data: DayShiftSettingsCreate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Set custom shift times for a specific day"""
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Remove existing settings for this day
    existing = [ds for ds in schedule.day_settings if ds.day == data.day]
    for ds in existing:
        session.delete(ds)
    
    # Create new settings
    day_settings = DayShiftSettings(
        schedule_id=schedule_id,
        day=data.day,
        start_time=data.start_time,
        end_time=data.end_time,
        is_holiday=data.is_holiday
    )
    session.add(day_settings)
    session.commit()
    session.refresh(day_settings)
    
    return day_settings


# ==========================================
# Shifts Management
# ==========================================

@router.post("/{schedule_id}/shifts", response_model=ShiftRead)
async def add_shift(
    schedule_id: UUID,
    data: ShiftCreate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Add a shift to schedule"""
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    shift = Shift(
        schedule_id=schedule_id,
        doctor_id=data.doctor_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time
    )
    session.add(shift)
    session.commit()
    session.refresh(shift)
    
    result = ShiftRead.model_validate(shift)
    result.doctor_name = shift.doctor.full_name if shift.doctor else None
    return result


@router.patch("/shifts/{shift_id}", response_model=ShiftRead)
async def update_shift(
    shift_id: UUID,
    data: ShiftUpdate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Update a shift"""
    shift = session.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shift, key, value)
    
    session.add(shift)
    session.commit()
    session.refresh(shift)
    
    result = ShiftRead.model_validate(shift)
    result.doctor_name = shift.doctor.full_name if shift.doctor else None
    return result


@router.delete("/shifts/{shift_id}")
async def delete_shift(
    shift_id: UUID,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Delete a shift"""
    shift = session.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    
    session.delete(shift)
    session.commit()
    return {"message": "Shift deleted"}