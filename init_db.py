from sqlalchemy.orm import sessionmaker

from app.core.database import engine, SessionLocal
from app.config.settings import Base
from app.models import device, detected_device, device_log, sensor_data, user, automation
from app.models.user import User
from app.core.security import create_access_token, verify_password, get_password_hash
def add_default_user():
    session = SessionLocal()
    try:
        default_user = User(username="admin", hashed_password=get_password_hash("admin"), is_admin=True)
        session.add(default_user)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

# Crée les tables dans la base de données
if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")

    add_default_user()
