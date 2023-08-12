from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.crud.base import CRUDBase

class CRUDProduct(CRUDBase):
    pass

product = CRUDProduct(Product)
