from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.detected_device import DetectedDevices
from app.core.modbus_thread import client_list
from app.services.modbus import Client

def create_device_endpoint(db: Session, detected_device_id: int, name: str):
    detected_device = db.query(DetectedDevices).filter(DetectedDevices.id == detected_device_id).first()
    ip = detected_device.ip
    new_device = Device(name=name, ip=ip, type=detected_device.type, device_metadata=detected_device.device_metadata, is_alive=True)
    
    global client_list
    client_list |= {ip : Client(ip)}

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
    global client_list
    client_list.pop(device.ip)

    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}

def update_device_by_id_endpoint(db, device_id, name):
    device = db.query(Device).filter(Device.id == device_id).first()
    device.name = name
    db.commit()
    return {"message": "Device updated successfully"}
