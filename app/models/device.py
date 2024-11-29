from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.config.settings import Base
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"  # Nom de la table dans la base de données

    id = Column(Integer, primary_key=True, index=True)  # Clé primaire
    name = Column(String, nullable=False)              # Nom de l'appareil
    type = Column(String, nullable=False)              # Type de l'appareil (e.g., sensor, switch)
    device_metadata = Column(JSON, default={})                # Métadonnées supplémentaires (JSON)
    last_seen = Column(DateTime, default=datetime.utcnow)  # Dernière communication
