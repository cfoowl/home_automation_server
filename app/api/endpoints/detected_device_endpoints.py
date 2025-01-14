from sqlalchemy.orm import Session
from app.models.detected_device import DetectedDevices
from app.services.scan_devices import scan_devices

def delete_detected_device_by_id_endpoint(db: Session, detected_device_id: int):
    device = db.query(DetectedDevices).filter(DetectedDevices.id == detected_device_id).first()
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}


def get_all_detected_devices_endpoint(db: Session):
    return db.query(DetectedDevices).all()

def start_new_scan_endpoint(db : Session):
    return scan_devices(db)