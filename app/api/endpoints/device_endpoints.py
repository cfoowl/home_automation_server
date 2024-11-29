from sqlalchemy.orm import Session
from app.models.device import Device

def create_device(db: Session, name: str, type: str, metadata: dict = {}):
    new_device = Device(name=name, type=type, device_metadata=metadata)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return {"id": new_device.id, "name": new_device.name}
