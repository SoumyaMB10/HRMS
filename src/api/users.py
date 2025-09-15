from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.deps import get_db, get_current_user, require_role
from src.schemas.user import UserCreate, UserRead
from src.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserRead)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["line_manager", "hr", "hr_manager", "admin"]))
):
    return user_service.create_user(db, payload, current_user)

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_role(["hr", "hr_manager", "admin"]))):
    return user_service.list_users(db)
