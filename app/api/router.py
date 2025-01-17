from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.api.endpoints.device_endpoints import *
from app.api.endpoints.detected_device_endpoints import *
from app.api.endpoints.sensor_data_endpoints import *
from app.api.endpoints.device_actions_endpoints import *
from app.api.endpoints.device_logs_endpoints import *
from app.api.endpoints.user_endpoints import *

router = APIRouter()

# Detected Devices
@router.get("/detected-devices")
# current_user = Depends(get_current_user)
def get_detected_devices(db: Session = Depends(get_db)):
    return get_all_detected_devices_endpoint(db=db)

@router.post("/detected-devices/scan")
def scan_new_devices(db: Session = Depends(get_db)):
    return start_new_scan_endpoint(db=db)

@router.delete("/detected-device/{detected_device_id}")
def delete_detected_device(detected_device_id: int, db: Session = Depends(get_db)):
    return delete_detected_device_by_id_endpoint(db=db, detected_device_id=detected_device_id)

# Devices
@router.post("/devices")
def create_device(detected_device_id: int, name: str,  db: Session = Depends(get_db)):
    return create_device_endpoint(db=db, name=name, detected_device_id=detected_device_id)

@router.get("/devices")
def get_all_devices(db: Session = Depends(get_db)):
    return get_all_devices_endpoint(db=db)

@router.get("/device/{device_id}")
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return get_device_by_id_endpoint(db=db, device_id=device_id)

@router.delete("/device/{device_id}")
def delete_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return delete_device_by_id_endpoint(db=db, device_id=device_id)

@router.put("/device/{device_id}")
def update_device(device_id: int, name: str, db: Session = Depends(get_db)):
    return update_device_by_id_endpoint(db=db, device_id=device_id, name=name)

# Sensor Data
@router.get("/device/{device_id}/sensor_data/{limit}")
def get_sensor_data(device_id: int, limit: int, db: Session = Depends(get_db)):
    return get_last_sensor_data_entries_by_id(db=db, device_id=device_id, limit=limit)

# Device actions
@router.get("/device/{device_id}/actions")
def get_actions(device_id: int, db: Session = Depends(get_db)):
    return get_device_actions_by_id_endpoint(db=db, device_id=device_id)

@router.post("/device/{device_id}/action/{action_id}")
def post_action(device_id: int, action_id: int, db: Session = Depends(get_db)):
    return post_device_actions_by_id_endpoint(db=db, device_id=device_id, action_id=action_id)


# Device logs
@router.get("/device/{device_id}/logs/{limit}")
def get_logs(device_id: int, limit: int = 100, db: Session = Depends(get_db)):
    return get_device_logs_by_id_endpoint(db=db, device_id=device_id, limit=limit)

# Authentification

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    return login_endpoint(username=username, password=password, db = db)

@router.post("/users")
def create_user(username: str, password: str, is_admin: bool, db: Session = Depends(get_db)):
    return create_user_endpoint(username=username, password=password, is_admin=is_admin, db=db)
