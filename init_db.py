from app.core.database import engine
from app.config.settings import Base
from app.models import device, detected_device, device_log, sensor_data, user, automation


# Crée les tables dans la base de données
if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")
