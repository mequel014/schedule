# ./app/modules/preferences/models.py

from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.modules.users.models import User


class DayPreference(SQLModel, table=True):
    __tablename__ = "day_preference"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    year: int = Field(index=True)
    month: int = Field(index=True)
    day: int = Field(ge=1, le=31)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: "User" = Relationship(back_populates="preferences")