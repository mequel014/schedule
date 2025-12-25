# ./app/modules/users/utils.py

from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID

from .models import User
from .enums import UserRole
from app.core.security import get_password_hash, generate_password


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
    return session.get(User, user_id)


def get_all_users(session: Session, role: Optional[UserRole] = None) -> List[User]:
    statement = select(User)
    if role:
        statement = statement.where(User.role == role)
    return session.exec(statement).all()


def create_user(
    session: Session,
    email: str,
    full_name: str,
    role: UserRole = UserRole.DOCTOR,
    telegram_username: Optional[str] = None
) -> tuple[User, str]:
    """Create user and return (user, plain_password)"""
    plain_password = generate_password()
    hashed_password = get_password_hash(plain_password)
    
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=role,
        telegram_username=telegram_username
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user, plain_password


def reset_user_password(session: Session, user: User) -> str:
    """Reset password and return new plain password"""
    plain_password = generate_password()
    user.hashed_password = get_password_hash(plain_password)
    session.add(user)
    session.commit()
    return plain_password