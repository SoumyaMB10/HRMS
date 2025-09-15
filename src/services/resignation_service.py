from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from src.models.resignation import ResignationRequest
from src.schemas.resignation import ResignationSubmit

def submit_resignation(db: Session, user_id: int, payload: ResignationSubmit):
    try:
        res = ResignationRequest(
            user_id=user_id,
            notice_period_days=payload.notice_period_days,
            reason=payload.reason,
            status="pending",
            approver_level=1,
            created_at=datetime.utcnow()
        )
        db.add(res)
        db.commit()
        db.refresh(res)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resignation submission failed: {str(e)}")

def approve_resignation(db: Session, res_id: int, role: str):
    res = db.query(ResignationRequest).filter(ResignationRequest.id == res_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resignation not found")
    if role == "manager" and res.approver_level == 1:
        res.approver_level = 2
    elif role == "hr" and res.approver_level == 2:
        res.approver_level = 3
    elif role == "cfo" and res.approver_level == 3:
        res.status = "approved"
    else:
        raise HTTPException(status_code=403, detail="Not authorized to approve at this stage")
    db.commit()
    db.refresh(res)
    return res

def reject_resignation(db: Session, res_id: int, role: str):
    res = db.query(ResignationRequest).filter(ResignationRequest.id == res_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resignation not found")
    res.status = "rejected"
    db.commit()
    db.refresh(res)
    return res

def list_resignations(db: Session):
    return db.query(ResignationRequest).all()
