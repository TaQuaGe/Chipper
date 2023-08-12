from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.schemas.cart import CartCreate
from app.crud.base import CRUDBase

class CRUDCart(CRUDBase):
    pass

cart = CRUDCart(Cart)
