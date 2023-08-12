from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, Review
from app.services.review import create_review, get_review, update_review, delete_review

router = APIRouter()

@router.post("/reviews/", response_model=Review)
def create_product_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    return create_review(db, review)

@router.get("/reviews/{review_id}", response_model=Review)
def read_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    return get_review(db, review_id)

@router.put("/reviews/{review_id}", response_model=Review)
def update_product_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db)
):
    return update_review(db, review_id, review)

@router.delete("/reviews/{review_id}", response_model=Review)
def delete_product_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    return delete_review(db, review_id)
