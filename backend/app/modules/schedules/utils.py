# ./app/modules/schedules/utils.py

from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import date, time, timedelta
import calendar

from .models import Schedule, DayShiftSettings
from app.modules.shifts.models import Shift
from app.modules.preferences.models import DayPreference
from app.core.config import settings


def get_schedule(session: Session, year: int, month: int) -> Optional[Schedule]:
    statement = select(Schedule).where(
        Schedule.year == year,
        Schedule.month == month
    )
    return session.exec(statement).first()


def get_or_create_schedule(session: Session, year: int, month: int) -> Schedule:
    schedule = get_schedule(session, year, month)
    if not schedule:
        schedule = Schedule(year=year, month=month)
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
    return schedule


def get_default_shift_times(day_date: date, schedule: Schedule) -> tuple[time, time]:
    """Get default shift times for a date"""
    # Check for custom settings
    if schedule:
        for ds in schedule.day_settings:
            if ds.day == day_date.day:
                return ds.start_time, ds.end_time
    
    # Weekend (Saturday=5, Sunday=6)
    if day_date.weekday() >= 5:
        return time(settings.WEEKEND_START_HOUR, settings.WEEKEND_START_MINUTE), \
               time(settings.WEEKEND_END_HOUR, settings.WEEKEND_END_MINUTE)
    
    # Weekday
    return time(settings.WEEKDAY_START_HOUR, settings.WEEKDAY_START_MINUTE), \
           time(settings.WEEKDAY_END_HOUR, settings.WEEKDAY_END_MINUTE)


def is_weekend_or_holiday(day_date: date, schedule: Schedule) -> bool:
    """Check if day is weekend or marked as holiday"""
    if day_date.weekday() >= 5:
        return True
    
    if schedule:
        for ds in schedule.day_settings:
            if ds.day == day_date.day and ds.is_holiday:
                return True
    
    return False


def get_shifts_for_day(session: Session, schedule_id: UUID, day_date: date) -> List[Shift]:
    statement = select(Shift).where(
        Shift.schedule_id == schedule_id,
        Shift.date == day_date
    )
    return session.exec(statement).all()


def get_doctor_shifts_in_schedule(
    session: Session, 
    schedule_id: UUID, 
    doctor_id: UUID
) -> List[Shift]:
    statement = select(Shift).where(
        Shift.schedule_id == schedule_id,
        Shift.doctor_id == doctor_id
    ).order_by(Shift.date)
    return session.exec(statement).all()


def get_preferences_for_month(session: Session, year: int, month: int) -> List[DayPreference]:
    statement = select(DayPreference).where(
        DayPreference.year == year,
        DayPreference.month == month
    )
    return session.exec(statement).all()