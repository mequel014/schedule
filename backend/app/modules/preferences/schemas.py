# ./app/modules/preferences/schemas.py

from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class PreferenceCreate(BaseModel):
    year: int
    month: int
    days: List[int]  # List of days (1-31)


class PreferenceRead(BaseModel):
    id: UUID
    user_id: UUID
    year: int
    month: int
    day: int
    
    class Config:
        from_attributes = True


class MonthPreferences(BaseModel):
    year: int
    month: int
    days: List[int]