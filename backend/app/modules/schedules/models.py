# ./app/modules/schedules/models.py

from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, time

if TYPE_CHECKING:
    from app.modules.shifts.models import Shift


class Schedule(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    year: int = Field(index=True)
    month: int = Field(index=True)  # 1-12
    is_visible: bool = Field(default=False)  # Visible to doctors (draft mode)
    is_published: bool = Field(default=False)  # Fully published
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    shifts: List["Shift"] = Relationship(
        back_populates="schedule",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    day_settings: List["DayShiftSettings"] = Relationship(
        back_populates="schedule",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class DayShiftSettings(SQLModel, table=True):
    """Custom shift times for specific days"""
    __tablename__ = "day_shift_settings"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    schedule_id: UUID = Field(foreign_key="schedule.id", index=True)
    day: int = Field(ge=1, le=31)  # Day of month
    start_time: time
    end_time: time  # Next day if less than start_time
    is_holiday: bool = Field(default=False)  # Treat as weekend (full day)
    
    schedule: "Schedule" = Relationship(back_populates="day_settings")