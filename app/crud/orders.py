from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate
from app.crud.base import CRUDBase

class CRUDOrder(CRUDBase):
    pass

order = CRUDOrder(Order)
