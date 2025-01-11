from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.endpoints.device_endpoints import *
from app.api.endpoints.detected_device_endpoints import *
from app.api.endpoints.sensor_data_endpoints import *
from app.api.endpoints.device_actions import *

router = APIRouter()

# Detected Devices
@router.get("/detected-devices")
def get_detected_devices(db: Session = Depends(get_db)):
    return get_all_detected_devices_endpoint(db=db)
@router.post("/detected-devices/scan")
def scan_new_devices():
    pass
@router.delete("/detected-devices/{detected_device_id}")
def delete_detected_device(detected_device_id: int, db: Session = Depends(get_db)):
    return delete_detected_device_by_id_endpoint(db=db, detected_device_id=detected_device_id)

# Devices
@router.post("/devices/")
def create_device(detected_device_id: int, name: str,  db: Session = Depends(get_db)):
    return create_device_endpoint(db=db, name=name, detected_device_id=detected_device_id)

@router.get("/devices/")
def get_all_devices(db: Session = Depends(get_db)):
    return get_all_devices_endpoint(db=db)

@router.get("/devices/{device_id}")
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return get_device_by_id_endpoint(db=db, device_id=device_id)

@router.delete("/devices/{device_id}")
def delete_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return delete_device_by_id_endpoint(db=db, device_id=device_id)

@router.put("/devices/{device_id}")
def update_device(device_id: int, name: str, db: Session = Depends(get_db)):
    return update_device_by_id_endpoint(db=db, device_id=device_id, name=name)

# Sensor Data
@router.get("/devices/{device_id}/sensor_data/{limit}")
def get_sensor_data(device_id: int, limit: int, db: Session = Depends(get_db)):
    return get_last_sensor_data_entries_by_id(db=db, device_id=device_id, limit=limit)

# @router.post("/sensor-data/{data_type}/{device_id}/{value}")
# def test(device_id: int, data_type: str, value: float, db: Session = Depends(get_db)):
#     new_data = SensorData(device_id=device_id, data_type=data_type, value=value)
#     db.add(new_data)
#     db.commit()
#     db.refresh(new_data)
#     return new_data

# Device actions
@router.get("/devices/{device_id}/actions")
def get_actions(device_id: int, db: Session = Depends(get_db)):
    return get_device_actions_by_id_endpoint(db=db, device_id=device_id)

@router.post("/devices/actions/{action_id}")
def post_action(action_id: int, db: Session = Depends(get_db)):
    pass