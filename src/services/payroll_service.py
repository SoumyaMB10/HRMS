from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from src.models.payroll import PayrollRecord
from src.schemas.payroll import PayrollGenerate

def generate_payroll(db: Session, payload: PayrollGenerate):
    try:
        net = payload.gross - (payload.deductions or 0.0)
        payroll = PayrollRecord(
            user_id=payload.user_id,
            period=payload.period,
            gross=payload.gross,
            deductions=payload.deductions or 0.0,
            net=net,
            created_at=datetime.utcnow()
        )
        db.add(payroll)
        db.commit()
        db.refresh(payroll)
        return payroll
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payroll generation failed: {str(e)}")

def list_payrolls(db: Session):
    return db.query(PayrollRecord).all()

def get_user_payrolls(db: Session, user_id: int):
    return db.query(PayrollRecord).filter(PayrollRecord.user_id == user_id).all()
