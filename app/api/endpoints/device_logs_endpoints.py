from sqlalchemy.orm import Session
from app.models.device_log import DeviceLog

def get_device_logs_by_id_endpoint(db: Session, device_id: int, limit: int = 100):
    return db.query(DeviceLog).filter(DeviceLog.device_id == device_id).limit(limit).all()
