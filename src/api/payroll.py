from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.deps import get_db, get_current_user, require_role
from src.services import payroll_service
from src.schemas.payroll import PayrollGenerate, PayrollRead

router = APIRouter(prefix="/api/payroll", tags=["payroll"])

# Only HR can generate payroll
@router.post("/generate", response_model=PayrollRead)
def api_generate_payroll(
    payload: PayrollGenerate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr"]))
):
    return payroll_service.generate_payroll(db, payload)

# Employees can only see their payroll
@router.get("/{user_id}", response_model=List[PayrollRead])
def api_get_user_payrolls(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == "employee" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view other employees' payrolls")
    return payroll_service.get_user_payrolls(db, user_id)

@router.get("/", response_model=List[PayrollRead])
def api_list_payrolls(db: Session = Depends(get_db)):
    return payroll_service.list_payrolls(db)


