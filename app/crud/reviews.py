from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.crud.base import CRUDBase

class CRUDReview(CRUDBase):
    pass

review = CRUDReview(Review)
