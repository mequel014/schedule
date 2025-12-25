# ./app/modules/swap_requests/models.py

from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.shifts.models import Shift


class SwapRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SwapRequestType(str, Enum):
    SWAP = "swap"      # Exchange with another doctor
    CANCEL = "cancel"  # Cancel shift


class SwapRequest(SQLModel, table=True):
    __tablename__ = "swap_request"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    requester_id: UUID = Field(foreign_key="user.id", index=True)
    shift_id: UUID = Field(foreign_key="shift.id", index=True)
    request_type: SwapRequestType
    target_doctor_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    target_shift_id: Optional[UUID] = Field(default=None, foreign_key="shift.id")
    status: SwapRequestStatus = Field(default=SwapRequestStatus.PENDING)
    comment: Optional[str] = None
    admin_comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    
    # Relationships
    requester: "User" = Relationship(
        back_populates="swap_requests_from",
        sa_relationship_kwargs={"foreign_keys": "[SwapRequest.requester_id]"}
    )
    target_doctor: Optional["User"] = Relationship(
        back_populates="swap_requests_to",
        sa_relationship_kwargs={"foreign_keys": "[SwapRequest.target_doctor_id]"}
    )