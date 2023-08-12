from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.base import CRUDBase

class CRUDUser(CRUDBase):
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

user = CRUDUser(User)
