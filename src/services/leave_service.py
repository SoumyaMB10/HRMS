from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.leave import LeaveRequest
from datetime import date

def apply_leave(db: Session, payload):
    try:
        if payload.start_date > payload.end_date:
            raise HTTPException(status_code=400, detail="start_date cannot be after end_date")
        lr = LeaveRequest(
            user_id=payload.user_id,
            leave_type=payload.leave_type,
            start_date=payload.start_date,
            end_date=payload.end_date,
            reason=payload.reason,
            half_day=payload.half_day or False,
            half_day_type=payload.half_day_type,
            status="pending",
            approver_level=1
        )
        db.add(lr)
        db.commit()
        db.refresh(lr)
        # TODO: notify manager asynchronously
        return {"message": "Leave applied successfully", "leave_id": lr.id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Apply leave failed: {str(e)}")

def get_leave_calendar(month: int, year: int):
    try:
        items = []
        items.append({"date": f"{year}-{month:02d}-01", "reason": "Month Start"})
        items.append({"date": f"{year}-{month:02d}-15", "reason": "Company Holiday"})
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get leave calendar failed: {str(e)}")
