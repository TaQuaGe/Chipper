from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.models import base
from app.api.routes import authentication, products, cart, users, orders, reviews, miscellaneous
from sqlalchemy.orm import Session
from app.config import Settings
from app.db.session import engine, Base
from app import models

app = FastAPI()


origins = [
    "http://localhost:3000"
]


@lru_cache()
def get_settings():
    return Settings()



settings = Settings()

def create_app() -> FastAPI:
    
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

    # Include API routes
    app.include_router(authentication.router, tags=["authentication"], prefix="/auth")
    app.include_router(products.router, tags=["products"], prefix="/products")
    app.include_router(cart.router, tags=["cart"], prefix="/cart")
    app.include_router(users.router, tags=["users"], prefix="/users")
    app.include_router(orders.router, tags=["orders"], prefix="/orders")
    app.include_router(reviews.router, tags=["reviews"], prefix="/reviews")
    app.include_router(miscellaneous.router, tags=["miscellaneous"], prefix="/misc")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Main"])
def read_root():
    return {"message": "Welcome to the Chipper API"}

