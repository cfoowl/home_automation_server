from sqlalchemy import Column, Integer, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from app.config.settings import Base

class Automation(Base):
    __tablename__ = "automation"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("device.id", ondelete="CASCADE"), nullable=False)
    sensor_type = Column(String, nullable=False)
    condition = Column(JSON, nullable=False)
    actuator_id = Column(Integer, ForeignKey("device.id", ondelete="CASCADE"), nullable=False)
    action_id = Column(Integer, nullable=False)
    # Relationships
    device = relationship("Device", back_populates="sensor_data")