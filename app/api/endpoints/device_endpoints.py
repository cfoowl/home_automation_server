from sqlalchemy.orm import Session
from app.models.device import Device

def create_device_endpoint(db: Session, name: str, type: str, metadata: dict = {}):
    new_device = Device(name=name, type=type, device_metadata=metadata)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return {"id": new_device.id, "name": new_device.name}

def get_all_devices_endpoint(db: Session):
    return db.query(Device).all()

def get_device_by_id_endpoint(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

def delete_device_by_id_endpoint(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}
