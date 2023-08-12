from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserInDB
from app.schemas.cart import CartItemCreate
from app.services.cart import add_product_to_cart, get_cart, remove_product_from_cart
from app.services.authentication import get_current_user

router = APIRouter()

@router.post("/cart", response_model=UserInDB)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    return add_product_to_cart(db, user, item)

@router.get("/cart", response_model=UserInDB)
def get_user_cart(
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    return get_cart(db, user)

@router.delete("/cart/{product_id}", response_model=UserInDB)
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(get_current_user)
):
    return remove_product_from_cart(db, user, product_id)
