from pydantic import BaseModel
from typing import Optional
from datetime import date

class LeaveApply(BaseModel):
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    half_day: Optional[bool] = False
    half_day_type: Optional[str] = None

class LeaveRead(BaseModel):
    id: int
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str
    approver_level: int
    class Config:
        orm_mode = True
