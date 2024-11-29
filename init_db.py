from app.core.database import engine
from app.models.device import Base

# Crée les tables dans la base de données
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")
