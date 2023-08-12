from typing import List, Optional
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate
from app.db.session import SessionLocal

def add_product_to_cart(
    db: SessionLocal,
    user: User,
    item: CartItemCreate
) -> Cart:
    cart = user.cart
    product = db.query(Product).filter(Product.id == item.product_id).first()
    cart_item = CartItem(quantity=item.quantity, product=product)
    cart.items.append(cart_item)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def get_cart(
    db: SessionLocal,
    user: User
) -> Optional[Cart]:
    return user.cart

def remove_product_from_cart(
    db: SessionLocal,
    user: User,
    product_id: int
) -> Cart:
    cart = user.cart
    cart.items = [item for item in cart.items if item.product_id != product_id]
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart
