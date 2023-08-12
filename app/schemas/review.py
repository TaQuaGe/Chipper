from pydantic import BaseModel

class ReviewBase(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str = None

class ReviewCreate(ReviewBase):
    pass
class ReviewUpdate(ReviewBase):
    pass
class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
