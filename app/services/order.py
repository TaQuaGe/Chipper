from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB


def create_order(db: Session, user: User, order: OrderCreate) -> OrderInDB:
    order_data = order.dict(exclude_unset=True)
    order_data["user_id"] = user.id
    db_order = Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int, user: User) -> OrderInDB:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    return order


def get_user_orders(db: Session, user: User, skip: int = 0, limit: int = 10) -> list[OrderInDB]:
    orders = db.query(Order).filter(Order.user_id == user.id).offset(skip).limit(limit).all()
    return orders


def update_order_status(db: Session, user: User, order_id: int, status: str) -> OrderInDB:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        return None

    setattr(order, "status", status)
    db.commit()
    db.refresh(order)
    return order
