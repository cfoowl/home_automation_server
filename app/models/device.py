from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.settings import Base
from datetime import datetime
from app.models.sensor_data import SensorData
from app.models.device_log import DeviceLog

class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    type = Column(String, nullable=False)
    device_metadata = Column(JSON, default={})
    registered_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen = Column(DateTime(timezone=True), default=datetime.now)
    # Relationships
    sensor_data = relationship("SensorData", back_populates="device", cascade="all, delete")
    log = relationship("DeviceLog", back_populates="device", cascade="all, delete")
    automation = relationship("Automation", back_populates="device", cascade="all, delete")