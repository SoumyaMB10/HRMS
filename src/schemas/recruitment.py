from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecruitmentCreate(BaseModel):
    role_title: str
    description: Optional[str] = None

class RecruitmentRead(BaseModel):
    id: int
    created_by: int
    role_title: str
    description: Optional[str]
    status: str
    approver_level: int
    created_at: datetime

    class Config:
        orm_mode = True
