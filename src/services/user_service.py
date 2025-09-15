from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.core import security
from src.schemas.user import UserCreate

def create_user(db: Session, payload: UserCreate, creator: User):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Role hierarchy rules
    if creator.role == "line_manager":
        # Can only create employees, and must assign themselves as manager
        if payload.role != "employee":
            raise HTTPException(status_code=403, detail="Line Manager can only create employees")
        payload.manager_id = creator.id

    elif creator.role == "hr":
        # Can create employees and line managers
        if payload.role not in ["employee", "line_manager"]:
            raise HTTPException(status_code=403, detail="HR cannot create this role")

    elif creator.role == "hr_manager":
        # Can create employees, line managers, and HR
        if payload.role not in ["employee", "line_manager", "hr"]:
            raise HTTPException(status_code=403, detail="HR Manager cannot create this role")

    elif creator.role == "admin":
        # Admin can create anyone
        pass
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to create users")

    hashed_pw = security.hash_password(payload.password)
    user = User(
        email=payload.email,
        role=payload.role,
        hashed_password=hashed_pw,
        manager_id=payload.manager_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session):
    return db.query(User).all()
