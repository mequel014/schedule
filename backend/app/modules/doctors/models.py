# ./app/modules/doctors/models.py

from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.modules.users.models import User


class DoctorProfile(SQLModel, table=True):
    __tablename__ = "doctor_profile"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    priority: int = Field(default=1, ge=1, le=10)  # 1-10, higher = more priority
    min_shifts_per_month: int = Field(default=4, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: "User" = Relationship(back_populates="doctor_profile")