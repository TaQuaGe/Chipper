# app/database/session.py
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.config import Settings
from sqlalchemy.ext.declarative import declarative_base
settings = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Export the 'db' object for use in other modules
db = SessionLocal()
