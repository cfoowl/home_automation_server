from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.endpoints.device_endpoints import *

router = APIRouter()

@router.post("/devices/")
def create_device(name: str, type: str, metadata: dict = {}, db: Session = Depends(get_db)):
    return create_device_endpoint(db=db, name=name, type=type, metadata=metadata)

@router.get("/devices/")
def get_all_devices(db: Session = Depends(get_db)):
    return get_all_devices_endpoint(db=db)

@router.get("/devices/{device_id}")
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return get_device_by_id_endpoint(db=db, device_id=device_id)

@router.delete("/devices/{device_id}")
def delete_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return delete_device_by_id_endpoint(db=db, device_id=device_id)