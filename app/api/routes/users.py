from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.services.user import (
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    return get_user_by_id(db, user_id)

@router.get("/users/", response_model=list[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users."""
    return get_all_users(db, skip, limit)

@router.post("/users/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    return create_user(db, user)

@router.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update a user."""
    return update_user(db, user_id, user_update)

@router.delete("/users/{user_id}", response_model=UserInDB)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user."""
    return delete_user(db, user_id)
