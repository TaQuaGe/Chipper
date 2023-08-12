from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_password, get_password_hash, create_access_token, decode_jwt_token
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.services.authentication import authenticate_user, get_current_user, create_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register/", response_model=UserInDB)
def register_user(user: UserCreate):
    # Check if user already exists
    existing_user = User.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the user in the database
    new_user = create_user(user, hashed_password)
    return new_user

@router.post("/token/")
def login_user(email: str = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create and return the JWT token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/")
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
