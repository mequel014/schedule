# ./app/modules/users/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.core.db import get_session
from app.core.security import (
    get_current_user, 
    get_current_admin, 
    get_current_sysadmin,
    verify_password,
    get_password_hash,
    create_access_token
)
from .models import User
from .schemas import (
    UserCreate, UserUpdate, UserRead, UserWithProfile,
    UserRoleUpdate, UserPasswordChange, Token, LoginRequest
)
from .enums import UserRole
from . import utils
from app.modules.doctors.models import DoctorProfile

router = APIRouter(prefix="/api", tags=["users"])


# ==========================================
# Auth
# ==========================================

@router.post("/auth/login", response_model=Token)
async def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = utils.get_user_by_email(session, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


# ==========================================
# Current User
# ==========================================

@router.get("/users/me", response_model=UserWithProfile)
async def get_me(current_user: User = Depends(get_current_user)):
    result = UserWithProfile.model_validate(current_user)
    if current_user.doctor_profile:
        result.priority = current_user.doctor_profile.priority
        result.min_shifts_per_month = current_user.doctor_profile.min_shifts_per_month
    return result


@router.patch("/users/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    update_data = data.model_dump(exclude_unset=True)
    # Users can't change their own is_active status
    update_data.pop("is_active", None)
    
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.post("/users/me/password/change")
async def change_password(
    data: UserPasswordChange,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.hashed_password = get_password_hash(data.new_password)
    session.add(current_user)
    session.commit()
    return {"message": "Password changed successfully"}


# ==========================================
# Admin: User Management
# ==========================================

@router.get("/users", response_model=List[UserWithProfile])
async def list_users(
    role: UserRole = None,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    users = utils.get_all_users(session, role)
    result = []
    for user in users:
        user_data = UserWithProfile.model_validate(user)
        if user.doctor_profile:
            user_data.priority = user.doctor_profile.priority
            user_data.min_shifts_per_month = user.doctor_profile.min_shifts_per_month
        result.append(user_data)
    return result


@router.post("/users", response_model=dict)
async def create_user(
    data: UserCreate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    # Check if email exists
    if utils.get_user_by_email(session, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Only sysadmin can create admins/sysadmins
    if data.role in [UserRole.ADMIN, UserRole.SYSADMIN]:
        if current_user.role != UserRole.SYSADMIN:
            raise HTTPException(status_code=403, detail="Only sysadmin can create admins")
    
    user, plain_password = utils.create_user(
        session=session,
        email=data.email,
        full_name=data.full_name,
        role=data.role,
        telegram_username=data.telegram_username
    )
    
    # Create doctor profile for doctors
    if data.role == UserRole.DOCTOR or data.role == UserRole.SYSADMIN:
        profile = DoctorProfile(
            user_id=user.id,
            priority=data.priority,
            min_shifts_per_month=data.min_shifts_per_month
        )
        session.add(profile)
        session.commit()
    
    return {
        "user": UserRead.model_validate(user),
        "generated_password": plain_password
    }


@router.get("/users/{user_id}", response_model=UserWithProfile)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    user = utils.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = UserWithProfile.model_validate(user)
    if user.doctor_profile:
        result.priority = user.doctor_profile.priority
        result.min_shifts_per_month = user.doctor_profile.min_shifts_per_month
    return result


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    user = utils.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/users/{user_id}/reset-password")
async def reset_password(
    user_id: UUID,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    user = utils.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_password = utils.reset_user_password(session, user)
    return {"new_password": new_password}


# ==========================================
# Sysadmin: Role Management
# ==========================================

@router.patch("/users/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: UUID,
    data: UserRoleUpdate,
    current_user: User = Depends(get_current_sysadmin),
    session: Session = Depends(get_session)
):
    user = utils.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = data.role
    
    # Create doctor profile if becoming doctor and doesn't have one
    if data.role in [UserRole.DOCTOR, UserRole.SYSADMIN] and not user.doctor_profile:
        profile = DoctorProfile(user_id=user.id)
        session.add(profile)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user