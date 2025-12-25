# ./app/modules/users/models.py

from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from .enums import UserRole

if TYPE_CHECKING:
    from app.modules.doctors.models import DoctorProfile
    from app.modules.preferences.models import DayPreference
    from app.modules.shifts.models import Shift
    from app.modules.swap_requests.models import SwapRequest


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: str
    telegram_username: Optional[str] = None
    role: UserRole = Field(default=UserRole.DOCTOR)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    doctor_profile: Optional["DoctorProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"}
    )
    preferences: List["DayPreference"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    shifts: List["Shift"] = Relationship(
        back_populates="doctor",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    swap_requests_from: List["SwapRequest"] = Relationship(
        back_populates="requester",
        sa_relationship_kwargs={
            "foreign_keys": "[SwapRequest.requester_id]",
            "cascade": "all, delete-orphan"
        }
    )
    swap_requests_to: List["SwapRequest"] = Relationship(
        back_populates="target_doctor",
        sa_relationship_kwargs={
            "foreign_keys": "[SwapRequest.target_doctor_id]",
            "cascade": "all, delete-orphan"
        }
    )