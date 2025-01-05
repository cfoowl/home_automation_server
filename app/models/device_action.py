from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.settings import Base
from datetime import datetime

class DeviceAction(Base):
    __tablename__ = "device_action"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("device.id", ondelete="CASCADE"), nullable=False)
    action_name = Column(String, nullable=False)
    command = Column(String, nullable=False)
    # Relationship
    device = relationship("Device", back_populates="action")
