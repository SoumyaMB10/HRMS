from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.deps import get_db, get_current_user, require_role
from src.services import recruitment_service
from src.schemas.recruitment import RecruitmentCreate, RecruitmentRead

router = APIRouter(prefix="/api/recruitment", tags=["recruitment"])

@router.post("/", response_model=RecruitmentRead)
def api_create_recruitment(payload: RecruitmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return recruitment_service.create_recruitment(db, current_user.id, payload)

# Only HR and CFO can approve/reject recruitment
@router.post("/{req_id}/approve")
def api_approve_recruitment(
    req_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr", "cfo"]))
):
    return recruitment_service.approve_recruitment(db, req_id, current_user.role)

@router.post("/{req_id}/reject")
def api_reject_recruitment(
    req_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr", "cfo"]))
):
    return recruitment_service.reject_recruitment(db, req_id, current_user.role)


@router.get("/", response_model=List[RecruitmentRead])
def api_list_recruitments(db: Session = Depends(get_db)):
    return recruitment_service.list_recruitments(db)
