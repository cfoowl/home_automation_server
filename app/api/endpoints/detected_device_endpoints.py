from sqlalchemy.orm import Session
from app.models.detected_device import DetectedDevices

def delete_detected_device_by_id_endpoint(db: Session, detected_device_id: int):
    device = db.query(DetectedDevices).filter(DetectedDevices.id == detected_device_id).first()
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}


def get_all_detected_devices_endpoint(db: Session):
    return db.query(DetectedDevices).all()
