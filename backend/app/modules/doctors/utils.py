# ./app/modules/doctors/utils.py

from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import date

from .models import DoctorProfile
from app.modules.users.models import User
from app.modules.users.enums import UserRole
from app.modules.shifts.models import Shift


def get_doctor_profile(session: Session, user_id: UUID) -> Optional[DoctorProfile]:
    statement = select(DoctorProfile).where(DoctorProfile.user_id == user_id)
    return session.exec(statement).first()


def get_all_doctors(session: Session) -> List[User]:
    """Get all users who are doctors (have doctor profile)"""
    statement = select(User).where(
        User.role.in_([UserRole.DOCTOR, UserRole.SYSADMIN]),
        User.is_active == True
    )
    return session.exec(statement).all()


def calculate_shift_hours(shift: Shift) -> float:
    """Calculate hours for a shift"""
    start = shift.start_time
    end = shift.end_time
    
    # If end is next day (e.g., 16:00 to 09:00)
    if end <= start:
        hours = (24 - start.hour - start.minute / 60) + (end.hour + end.minute / 60)
    else:
        hours = (end.hour + end.minute / 60) - (start.hour + start.minute / 60)
    
    return hours


def get_doctor_stats(
    session: Session, 
    user_id: UUID, 
    year: int, 
    month: int
) -> dict:
    """Get statistics for a doctor for a specific month"""
    from app.modules.schedules.models import Schedule
    
    # Get schedule for the month
    statement = select(Schedule).where(
        Schedule.year == year,
        Schedule.month == month
    )
    schedule = session.exec(statement).first()
    
    if not schedule:
        return {"total_shifts": 0, "total_hours": 0.0}
    
    # Get shifts for this doctor in this schedule
    statement = select(Shift).where(
        Shift.schedule_id == schedule.id,
        Shift.doctor_id == user_id
    )
    shifts = session.exec(statement).all()
    
    total_hours = sum(calculate_shift_hours(shift) for shift in shifts)
    
    return {
        "total_shifts": len(shifts),
        "total_hours": total_hours
    }