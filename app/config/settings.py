from sqlalchemy.ext.declarative import declarative_base

# URL de connexion à la base de données
DATABASE_URL = "postgresql://myuser:azerty@localhost/domotique_test"

# Base pour les modèles SQLAlchemy
Base = declarative_base()
