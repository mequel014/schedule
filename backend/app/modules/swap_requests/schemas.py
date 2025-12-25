# ./app/modules/swap_requests/schemas.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from .models import SwapRequestStatus, SwapRequestType


class SwapRequestCreate(BaseModel):
    shift_id: UUID
    request_type: SwapRequestType
    target_doctor_id: Optional[UUID] = None
    target_shift_id: Optional[UUID] = None
    comment: Optional[str] = None


class SwapRequestResolve(BaseModel):
    status: SwapRequestStatus
    admin_comment: Optional[str] = None


class SwapRequestRead(BaseModel):
    id: UUID
    requester_id: UUID
    requester_name: Optional[str] = None
    shift_id: UUID
    shift_date: Optional[str] = None
    request_type: SwapRequestType
    target_doctor_id: Optional[UUID]
    target_doctor_name: Optional[str] = None
    target_shift_id: Optional[UUID]
    status: SwapRequestStatus
    comment: Optional[str]
    admin_comment: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True