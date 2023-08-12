from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

def create_review(db: Session, review: ReviewCreate) -> Review:
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int) -> Review:
    return db.query(Review).filter(Review.id == review_id).first()

def update_review(db: Session, review_id: int, review: ReviewUpdate) -> Review:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        for key, value in review.dict().items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        return db_review

def delete_review(db: Session, review_id: int) -> Review:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return db_review
