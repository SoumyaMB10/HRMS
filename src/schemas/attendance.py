from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceCreate(BaseModel):
    user_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AttendanceRead(BaseModel):
    id: int
    user_id: int
    login_time: datetime
    logout_time: Optional[datetime]
    total_hours: Optional[float]
    status: Optional[str]
    exception: Optional[str]
    class Config:
        orm_mode = True
