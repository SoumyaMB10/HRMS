from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.deps import get_db, get_current_user, require_role
from src.services import resignation_service
from src.schemas.resignation import ResignationSubmit, ResignationRead

router = APIRouter(prefix="/api/resignations", tags=["resignations"])

@router.post("/", response_model=ResignationRead)
def api_submit_resignation(payload: ResignationSubmit, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return resignation_service.submit_resignation(db, current_user.id, payload)

# Manager, HR, CFO can approve
@router.post("/{res_id}/approve")
def api_approve_resignation(
    res_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["manager", "hr", "cfo"]))
):
    return resignation_service.approve_resignation(db, res_id, current_user.role)

@router.post("/{res_id}/reject")
def api_reject_resignation(res_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return resignation_service.reject_resignation(db, res_id, current_user.role)

@router.get("/", response_model=List[ResignationRead])
def api_list_resignations(db: Session = Depends(get_db)):
    return resignation_service.list_resignations(db)
