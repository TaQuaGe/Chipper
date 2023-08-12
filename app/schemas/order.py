from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    status: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    quantity: Optional[int]
    status: Optional[str]


class OrderInDB(OrderBase):
    id: int

    class Config:
        orm_mode = True
