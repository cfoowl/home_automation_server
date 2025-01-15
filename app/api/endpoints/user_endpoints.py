from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token, verify_password, get_password_hash

def login_endpoint(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def create_user_endpoint(username: str, password: str, is_admin: bool, db: Session):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, is_admin=is_admin)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "is_admin": new_user.is_admin}