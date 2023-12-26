from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError

def get_user_by_id(db: Session, user_id: int) -> UserInDB:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user.dict())

def get_user_by_email(db: Session, email: str) -> UserInDB:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user.dict())

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserInDB]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserInDB(**user.dict()) for user in users]

def create_user(db: Session, user_create: UserCreate) -> UserInDB:
    try:
        hashed_password = get_password_hash(user_create.password)
        db_user = User(**user_create.dict(), hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserInDB(**db_user.dict())
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
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
    try:
        db_user = get_user_by_id(db, user_id)
        db.delete(db_user)
        db.commit()
        return UserInDB(**db_user.dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
