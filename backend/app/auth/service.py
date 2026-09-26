from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.password import hash_password, verify_password
from app.auth.schemas import LoginRequest, RegisterRequest
from app.database.models import User


def register_user(db: Session, data: RegisterRequest) -> User:
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        email=data.email,
        full_name=data.full_name,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, data: LoginRequest) -> str:
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if not user or not verify_password(data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    return create_access_token(user.id)