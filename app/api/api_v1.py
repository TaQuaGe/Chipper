from fastapi import APIRouter

from .routes import authentication, products, cart, users, orders, reviews, miscellaneous

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(products.router, tags=["products"], prefix="/products")
router.include_router(cart.router, tags=["cart"], prefix="/cart")
router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(orders.router, tags=["orders"], prefix="/orders")
router.include_router(reviews.router, tags=["reviews"], prefix="/reviews")
router.include_router(miscellaneous.router, tags=["miscellaneous"], prefix="/misc")
