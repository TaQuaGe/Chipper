from fastapi import APIRouter, Depends, HTTPException
from app.models.product import Product
from app.services.product import get_all_products, get_product_by_id

router = APIRouter()

@router.get("/")
async def get_products():
    """Get a list of all products."""
    products = await get_all_products()

    return products

@router.get("/id")
async def get_product_by_id(product_id: int):
    """Get a product by its ID."""
    product = await get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
