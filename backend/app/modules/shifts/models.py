# ./app/modules/shifts/models.py

from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date as date_type, time as time_type

if TYPE_CHECKING:
    from app.modules.schedules.models import Schedule
    from app.modules.users.models import User


class Shift(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    schedule_id: UUID = Field(foreign_key="schedule.id", index=True)
    doctor_id: UUID = Field(foreign_key="user.id", index=True)
    date: date_type = Field(index=True)
    start_time: time_type
    end_time: time_type
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    schedule: "Schedule" = Relationship(back_populates="shifts")
    doctor: "User" = Relationship(back_populates="shifts")