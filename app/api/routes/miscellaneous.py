# app/api/routes/miscellaneous.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "UP"}
