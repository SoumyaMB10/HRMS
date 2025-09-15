from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PayrollGenerate(BaseModel):
    user_id: int
    period: str   # e.g., "2025-09"
    gross: float
    deductions: Optional[float] = 0.0

class PayrollRead(BaseModel):
    id: int
    user_id: int
    period: str
    gross: float
    deductions: float
    net: float
    payslip_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
