from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.deps import get_db, get_current_user
from src.services.leave_service import apply_leave, get_leave_calendar
from src.services.manager_service import list_team_leaves, approve_leave, reject_leave
from src.schemas.leave import LeaveApply, LeaveRead
from typing import List

router = APIRouter(prefix="/api/leaves", tags=["leaves"])

@router.post("/apply")
def api_apply_leave(payload: LeaveApply, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if payload.user_id != current_user.id and current_user.role not in ("admin", "hr", "hr_manager"):
        raise HTTPException(status_code=403, detail="Cannot apply leave for another user")
    return apply_leave(db, payload)

@router.get("/calendar", response_model=List[dict])
def api_leave_calendar(month: int, year: int):
    return get_leave_calendar(month, year)

@router.get("/team", response_model=List[LeaveRead])
def api_team_leaves(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ("manager", "hr", "hr_manager", "admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    return list_team_leaves(db, current_user.id)

@router.post("/{leave_id}/approve")
def api_approve_leave(leave_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return approve_leave(db, leave_id, current_user.id)

@router.post("/{leave_id}/reject")
def api_reject_leave(leave_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return reject_leave(db, leave_id, current_user.id)
