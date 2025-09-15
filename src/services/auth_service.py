from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from src.models.user import User
from src.core import security

def authenticate_user(db: Session, identifier: str, password: str):
    if identifier.isdigit():
        user = db.query(User).filter(User.id == int(identifier)).first()
    else:
        user = db.query(User).filter(User.email == identifier).first()
    if not user or not security.verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, identifier: str, password: str):
    user = authenticate_user(db, identifier, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer", "role": user.role}
