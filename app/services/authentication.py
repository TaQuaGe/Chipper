import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_password, create_access_token, decode_jwt_token
from app.models.user import User
from app.schemas.user import UserInDB
from app.core.security import get_password_hash  # Import the get_password_hash function
from pydantic import ValidationError  # Import the ValidationError class


from datetime import timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(email: str, password: str) -> UserInDB:
    """Authenticate a user."""
    user = User.get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return user


def create_user(username: str, password: str):
    """Create a new user."""
    try:
        user = User(username=username, password=get_password_hash(password))
        user.create()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Get the current user from the access token."""
    try:
        payload = decode_jwt_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = User.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return UserInDB(**user.dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
