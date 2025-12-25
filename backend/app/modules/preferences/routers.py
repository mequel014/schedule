# ./app/modules/preferences/routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, delete
from typing import List
from uuid import UUID
from datetime import date

from app.core.db import get_session
from app.core.security import get_current_user
from app.modules.users.models import User
from .models import DayPreference
from .schemas import PreferenceCreate, PreferenceRead, MonthPreferences

router = APIRouter(prefix="/api/preferences", tags=["preferences"])


@router.get("/me", response_model=List[MonthPreferences])
async def get_my_preferences(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all my preferences grouped by month"""
    statement = select(DayPreference).where(
        DayPreference.user_id == current_user.id
    ).order_by(DayPreference.year, DayPreference.month, DayPreference.day)
    
    prefs = session.exec(statement).all()
    
    # Group by year/month
    grouped = {}
    for pref in prefs:
        key = (pref.year, pref.month)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(pref.day)
    
    return [
        MonthPreferences(year=year, month=month, days=days)
        for (year, month), days in grouped.items()
    ]


@router.get("/me/{year}/{month}", response_model=MonthPreferences)
async def get_my_month_preferences(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get my preferences for a specific month"""
    statement = select(DayPreference).where(
        DayPreference.user_id == current_user.id,
        DayPreference.year == year,
        DayPreference.month == month
    ).order_by(DayPreference.day)
    
    prefs = session.exec(statement).all()
    
    return MonthPreferences(
        year=year,
        month=month,
        days=[p.day for p in prefs]
    )


@router.post("/me", response_model=MonthPreferences)
async def set_my_preferences(
    data: PreferenceCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Set preferences for a month (replaces existing)"""
    # Delete existing preferences for this month
    statement = delete(DayPreference).where(
        DayPreference.user_id == current_user.id,
        DayPreference.year == data.year,
        DayPreference.month == data.month
    )
    session.exec(statement)
    
    # Add new preferences
    for day in data.days:
        pref = DayPreference(
            user_id=current_user.id,
            year=data.year,
            month=data.month,
            day=day
        )
        session.add(pref)
    
    session.commit()
    
    return MonthPreferences(
        year=data.year,
        month=data.month,
        days=data.days
    )


@router.post("/me/copy-from-previous")
async def copy_from_previous_month(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Copy preferences from previous month"""
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    
    # Get previous month preferences
    statement = select(DayPreference).where(
        DayPreference.user_id == current_user.id,
        DayPreference.year == prev_year,
        DayPreference.month == prev_month
    )
    prev_prefs = session.exec(statement).all()
    
    if not prev_prefs:
        raise HTTPException(status_code=404, detail="No preferences found for previous month")
    
    # Delete existing for target month
    statement = delete(DayPreference).where(
        DayPreference.user_id == current_user.id,
        DayPreference.year == year,
        DayPreference.month == month
    )
    session.exec(statement)
    
    # Copy days (validate they exist in target month)
    import calendar
    num_days = calendar.monthrange(year, month)[1]
    
    days = []
    for pref in prev_prefs:
        if pref.day <= num_days:
            new_pref = DayPreference(
                user_id=current_user.id,
                year=year,
                month=month,
                day=pref.day
            )
            session.add(new_pref)
            days.append(pref.day)
    
    session.commit()
    
    return MonthPreferences(year=year, month=month, days=days)