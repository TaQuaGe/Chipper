from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB

def get_user_by_id(db: Session, user_id: int) -> UserInDB:
    """
    Get a user by ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserInDB: The user information.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user.dict())

def get_user_by_email(db: Session, email: str) -> UserInDB:
    """
    Get a user by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        UserInDB: The user information.
    """
    user = db.query(User).filter(User.email == email).first()
    return UserInDB(**user.dict()) if user else None

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserInDB]:
    """
    Get all users.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to retrieve.

    Returns:
        list[UserInDB]: List of user information.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserInDB(**user.dict()) for user in users]

def create_user(db: Session, user: UserCreate) -> UserInDB:
    """
    Create a new user.

    Args:
        db (Session): The database session.
        user (UserCreate): The user information to create.

    Returns:
        UserInDB: The created user information.
    """
    try:
        # Ensure that 'password' is included in the UserCreate model.
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserInDB(**db_user.dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    """
    Update a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The updated user information.

    Returns:
        UserInDB: The updated user information.
    """
    try:
        db_user = get_user_by_id(db, user_id)
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return UserInDB(**db_user.dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_user(db: Session, user_id: int) -> UserInDB:
    """
    Delete a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        UserInDB: The deleted user information.
    """
    try:
        db_user = get_user_by_id(db, user_id)
        db.delete(db_user)
        db.commit()
        return UserInDB(**db_user.dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
