from sqlalchemy.orm import Session
from datetime import datetime, time as dtime
from fastapi import HTTPException
from src.models.attendance import Attendance
from src.models.user import User

WORK_START = dtime(hour=9, minute=30)  # example start time

def clock_in(db: Session, user_id: int, latitude: float | None, longitude: float | None):
    try:
        # create attendance
        rec = Attendance(user_id=user_id, login_time=datetime.utcnow(), latitude=latitude, longitude=longitude, status="online", exception=None)
        # detect late based on local time - simplified: compare UTC time's time component (for demo)
        if datetime.utcnow().time() > WORK_START:
            rec.exception = "late"
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clock-in failed: {str(e)}")

def clock_out(db: Session, user_id: int):
    try:
        rec = db.query(Attendance).filter(Attendance.user_id == user_id, Attendance.logout_time == None).order_by(Attendance.login_time.desc()).first()
        if not rec:
            raise HTTPException(status_code=404, detail="No active clock-in found")
        rec.logout_time = datetime.utcnow()
        diff = rec.logout_time - rec.login_time
        rec.total_hours = round(diff.total_seconds() / 3600, 2)
        rec.status = "offline"
        # if short day, mark exception
        if rec.total_hours < 4:
            rec.exception = (rec.exception or "") + (";short_day" if rec.exception else "short_day")
        db.commit()
        db.refresh(rec)
        return rec
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clock-out failed: {str(e)}")
