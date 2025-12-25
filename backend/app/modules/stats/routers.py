# ./app/modules/stats/routers.py

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from datetime import date

from app.core.db import get_session
from app.core.security import get_current_admin
from app.modules.users.models import User
from app.modules.users.enums import UserRole
from app.modules.doctors.utils import get_all_doctors, get_doctor_stats

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("/dashboard")
async def get_dashboard(
    year: int = None,
    month: int = None,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Get dashboard statistics for admins"""
    today = date.today()
    if not year:
        year = today.year
    if not month:
        month = today.month
    
    doctors = get_all_doctors(session)
    
    doctor_stats = []
    total_shifts = 0
    total_hours = 0.0
    
    for doctor in doctors:
        if not doctor.doctor_profile:
            continue
        
        stats = get_doctor_stats(session, doctor.id, year, month)
        
        doctor_stats.append({
            "id": str(doctor.id),
            "full_name": doctor.full_name,
            "email": doctor.email,
            "priority": doctor.doctor_profile.priority,
            "min_shifts_per_month": doctor.doctor_profile.min_shifts_per_month,
            "total_shifts": stats["total_shifts"],
            "total_hours": stats["total_hours"],
            "meets_minimum": stats["total_shifts"] >= doctor.doctor_profile.min_shifts_per_month
        })
        
        total_shifts += stats["total_shifts"]
        total_hours += stats["total_hours"]
    
    return {
        "year": year,
        "month": month,
        "summary": {
            "total_doctors": len(doctor_stats),
            "total_shifts": total_shifts,
            "total_hours": total_hours,
            "doctors_meeting_minimum": sum(1 for d in doctor_stats if d["meets_minimum"])
        },
        "doctors": doctor_stats
    }