from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB

def get_user_by_id(db: Session, user_id: int) -> UserInDB:
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user.dict())

def get_user_by_email(db: Session, email: str) -> UserInDB:
    """Get a user by email."""
    user = db.query(User).filter(User.email == email).first()
    return UserInDB(**user.dict()) if user else None

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserInDB]:
    """Get all users."""
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserInDB(**user.dict()) for user in users]

def create_user(db: Session, user: UserCreate) -> UserInDB:
    """Create a new user."""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInDB(**db_user.dict())

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    """Update a user."""
    db_user = get_user_by_id(db, user_id)
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return UserInDB(**db_user.dict())

def delete_user(db: Session, user_id: int) -> UserInDB:
    """Delete a user."""
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    return UserInDB(**db_user.dict())
