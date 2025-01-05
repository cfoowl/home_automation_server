from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.settings import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("device.id", ondelete="CASCADE"), nullable=False)
    data_type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    # Relationship
    device = relationship("Device", back_populates="sensor_data")
