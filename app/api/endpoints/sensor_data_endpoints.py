from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.sensor_data import SensorData

def get_last_sensor_data_entries_by_id(db: Session, device_id: int, limit: int):
    return db.query(SensorData).filter(SensorData.device_id == device_id).order_by(desc(SensorData.id)).limit(limit).all()

