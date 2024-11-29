from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# Dépendance pour obtenir la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
