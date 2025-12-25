# ./app/modules/users/schemas.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

from .enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    telegram_username: Optional[str] = None
    role: UserRole = UserRole.DOCTOR
    priority: int = 1
    min_shifts_per_month: int = 4


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    telegram_username: Optional[str] = None
    is_active: Optional[bool] = None


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str


class UserRead(BaseModel):
    id: UUID
    email: str
    full_name: str
    telegram_username: Optional[str]
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWithProfile(UserRead):
    priority: Optional[int] = None
    min_shifts_per_month: Optional[int] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str