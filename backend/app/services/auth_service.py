from sqlalchemy.orm import Session
from app.models.users import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

def signup_user(
    db: Session,
    email: str,
    username: str,
    password: str,
):
    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter((User.email == email) | (User.username == username))
        .first()
    )
    if existing_user:
        return None  # API layer decides how to respond

    user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    access_token = create_access_token({"sub": str(user.id)})

    return access_token
