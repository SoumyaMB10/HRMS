from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.deps import get_db, get_current_user
from src.services.policy_service import create_policy, acknowledge_policy
from src.schemas.policy import PolicyAcknowledge

router = APIRouter(prefix="/api/policies", tags=["policies"])

@router.post("/")
def api_create_policy(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ("hr", "hr_manager", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to create policies")
    title = payload.get("title")
    url = payload.get("document_url")
    mandatory = bool(payload.get("mandatory", False))
    return create_policy(db, title, url, mandatory)

@router.post("/acknowledge")
def api_acknowledge(payload: PolicyAcknowledge, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot acknowledge for another user")
    return acknowledge_policy(db, payload.user_id, payload.policy_id)
