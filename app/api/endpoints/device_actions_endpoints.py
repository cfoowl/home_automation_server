from sqlalchemy.orm import Session
from app.models.device_action import DeviceAction

def get_device_actions_by_id_endpoint(db: Session, device_id: int):
    return db.query(DeviceAction).filter(DeviceAction.device_id == device_id).all()
