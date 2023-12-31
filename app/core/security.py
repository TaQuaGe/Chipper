from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from app.config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  """Verifies a plain password against a hashed password."""
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  """Generates a hashed password from a plain password."""
  return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  """Creates an access token from a given payload."""
  settings = Settings()  # Initialize settings here

  SECRET_KEY = settings.SECRET_KEY
  ALGORITHM = settings.ALGORITHM
  ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_jwt_token(token: str):
  """Decodes an access token and returns the payload."""
  settings = Settings()  # Initialize settings here

  SECRET_KEY = settings.SECRET_KEY
  ALGORITHM = settings.ALGORITHM

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    return None
