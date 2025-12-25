# ./app/modules/schedules/schemas.py

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import date, time


class DayShiftSettingsCreate(BaseModel):
    day: int
    start_time: time
    end_time: time
    is_holiday: bool = False


class DayShiftSettingsRead(BaseModel):
    id: UUID
    day: int
    start_time: time
    end_time: time
    is_holiday: bool
    
    class Config:
        from_attributes = True


class ShiftCreate(BaseModel):
    doctor_id: UUID
    date: date
    start_time: time
    end_time: time


class ShiftUpdate(BaseModel):
    doctor_id: Optional[UUID] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class ShiftRead(BaseModel):
    id: UUID
    schedule_id: UUID
    doctor_id: UUID
    date: date
    start_time: time
    end_time: time
    doctor_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ScheduleCreate(BaseModel):
    year: int
    month: int


class ScheduleUpdate(BaseModel):
    is_visible: Optional[bool] = None
    is_published: Optional[bool] = None


class ScheduleRead(BaseModel):
    id: UUID
    year: int
    month: int
    is_visible: bool
    is_published: bool
    shifts: List[ShiftRead] = []
    day_settings: List[DayShiftSettingsRead] = []
    
    class Config:
        from_attributes = True


class DayInfo(BaseModel):
    date: date
    day_of_week: int  # 0=Monday, 6=Sunday
    is_weekend: bool
    is_holiday: bool
    default_start_time: time
    default_end_time: time
    shifts: List[ShiftRead] = []
    preferred_doctors: List[UUID] = []  # Doctors who want this day


class CalendarMonth(BaseModel):
    year: int
    month: int
    days: List[DayInfo]
    is_visible: bool
    is_published: bool