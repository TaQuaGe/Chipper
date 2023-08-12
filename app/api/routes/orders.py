from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB
from app.models.order import Order
from app.models.user import User
from app.services.order import create_order, get_order_by_id, get_user_orders, update_order_status
from app.services.authentication import get_current_user

router = APIRouter()

@router.post("/orders", response_model=OrderInDB)
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return create_order(db, user, order)

@router.get("/orders/{order_id}", response_model=OrderInDB)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    order = get_order_by_id(db, order_id, user)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.get("/orders", response_model=list[OrderInDB])
def get_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_user_orders(db, user, skip=skip, limit=limit)

@router.put("/orders/{order_id}", response_model=OrderInDB)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    updated_order = update_order_status(db, user, order_id, order.status)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order
