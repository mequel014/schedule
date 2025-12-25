# ./app/modules/doctors/schemas.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class DoctorProfileUpdate(BaseModel):
    priority: Optional[int] = None
    min_shifts_per_month: Optional[int] = None


class DoctorProfileRead(BaseModel):
    id: UUID
    user_id: UUID
    priority: int
    min_shifts_per_month: int
    
    class Config:
        from_attributes = True


class DoctorStats(BaseModel):
    user_id: UUID
    full_name: str
    total_shifts: int
    total_hours: float
    month: int
    year: int


class DoctorWithStats(BaseModel):
    id: UUID
    full_name: str
    email: str
    priority: int
    min_shifts_per_month: int
    current_month_shifts: int
    current_month_hours: float