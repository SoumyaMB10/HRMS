from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from src.models.recruitment import RecruitmentRequest
from src.schemas.recruitment import RecruitmentCreate

def create_recruitment(db: Session, user_id: int, payload: RecruitmentCreate):
    try:
        req = RecruitmentRequest(
            created_by=user_id,
            role_title=payload.role_title,
            description=payload.description,
            status="pending",
            approver_level=1,
            created_at=datetime.utcnow()
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        return req
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recruitment creation failed: {str(e)}")

def approve_recruitment(db: Session, req_id: int, role: str):
    req = db.query(RecruitmentRequest).filter(RecruitmentRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Recruitment not found")
    if role == "hr" and req.approver_level == 1:
        req.approver_level = 2
    elif role == "cfo" and req.approver_level == 2:
        req.status = "approved"
    else:
        raise HTTPException(status_code=403, detail="Not authorized to approve at this stage")
    db.commit()
    db.refresh(req)
    return req

def reject_recruitment(db: Session, req_id: int, role: str):
    req = db.query(RecruitmentRequest).filter(RecruitmentRequest.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Recruitment not found")
    req.status = "rejected"
    db.commit()
    db.refresh(req)
    return req

def list_recruitments(db: Session):
    return db.query(RecruitmentRequest).all()
