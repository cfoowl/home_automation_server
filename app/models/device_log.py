from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.settings import Base
from datetime import datetime

class DeviceLog(Base):
    __tablename__ = "device_log"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("device.id", ondelete="CASCADE"), nullable=False)
    log_type = Column(String, nullable=False)
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    # Relationship
    device = relationship("Device", back_populates="log")
