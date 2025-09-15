from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResignationSubmit(BaseModel):
    notice_period_days: Optional[int] = None
    reason: Optional[str] = None

class ResignationRead(BaseModel):
    id: int
    user_id: int
    notice_period_days: Optional[int]
    reason: Optional[str]
    status: str
    approver_level: int
    created_at: datetime

    class Config:
        orm_mode = True
