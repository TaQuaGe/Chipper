from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    username: str
    email: str
    hashed_password: str
    

class UserUpdate(UserBase):
    username: str
    email: str
    
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
