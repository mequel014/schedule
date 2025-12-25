# ./app/modules/doctors/routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import date

from app.core.db import get_session
from app.core.security import get_current_user, get_current_admin
from app.modules.users.models import User
from app.modules.users.enums import UserRole
from .models import DoctorProfile
from .schemas import DoctorProfileUpdate, DoctorProfileRead, DoctorWithStats
from . import utils

router = APIRouter(prefix="/api/doctors", tags=["doctors"])


@router.get("", response_model=List[DoctorWithStats])
async def list_doctors(
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """List all doctors with their current month stats"""
    doctors = utils.get_all_doctors(session)
    today = date.today()
    
    result = []
    for doctor in doctors:
        if not doctor.doctor_profile:
            continue
            
        stats = utils.get_doctor_stats(
            session, 
            doctor.id, 
            today.year, 
            today.month
        )
        
        result.append(DoctorWithStats(
            id=doctor.id,
            full_name=doctor.full_name,
            email=doctor.email,
            priority=doctor.doctor_profile.priority,
            min_shifts_per_month=doctor.doctor_profile.min_shifts_per_month,
            current_month_shifts=stats["total_shifts"],
            current_month_hours=stats["total_hours"]
        ))
    
    return result


@router.get("/me/stats")
async def get_my_stats(
    year: int = None,
    month: int = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current user's shift statistics"""
    today = date.today()
    if not year:
        year = today.year
    if not month:
        month = today.month
    
    stats = utils.get_doctor_stats(session, current_user.id, year, month)
    return {
        "year": year,
        "month": month,
        **stats
    }


@router.get("/me/stats/history")
async def get_my_stats_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get shift statistics history for current user"""
    today = date.today()
    history = []
    
    # Last 12 months
    for i in range(12):
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        
        stats = utils.get_doctor_stats(session, current_user.id, year, month)
        history.append({
            "year": year,
            "month": month,
            **stats
        })
    
    return history


@router.patch("/{user_id}/profile", response_model=DoctorProfileRead)
async def update_doctor_profile(
    user_id: UUID,
    data: DoctorProfileUpdate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Update doctor's priority and minimum shifts"""
    profile = utils.get_doctor_profile(session, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile