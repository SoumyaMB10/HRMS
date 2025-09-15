from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.deps import get_db, get_current_user
from src.services.attendance_service import clock_in, clock_out
from src.schemas.attendance import AttendanceCreate, AttendanceRead

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

@router.post("/clock-in", response_model=AttendanceRead)
def api_clock_in(payload: AttendanceCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if payload.user_id != current_user.id and current_user.role not in ("admin", "hr", "hr_manager"):
        raise HTTPException(status_code=403, detail="Cannot clock-in for another user")
    return clock_in(db, payload.user_id, payload.latitude, payload.longitude)

@router.post("/clock-out", response_model=AttendanceRead)
def api_clock_out(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if user_id != current_user.id and current_user.role not in ("admin", "hr", "hr_manager"):
        raise HTTPException(status_code=403, detail="Cannot clock-out for another user")
    return clock_out(db, user_id)
