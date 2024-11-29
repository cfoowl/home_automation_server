from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.endpoints.device_endpoints import create_device as create_device_endpoint

router = APIRouter()

@router.post("/devices/")
def create_device(name: str, type: str, metadata: dict = {}, db: Session = Depends(get_db)):
    return create_device_endpoint(db=db, name=name, type=type, metadata=metadata)
