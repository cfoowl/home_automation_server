from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.config.settings import Base
from datetime import datetime

class DetectedDevices(Base):
    __tablename__ = "detected_device"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    type = Column(String, nullable=False)
    device_metadata = Column(JSON, default={})
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
