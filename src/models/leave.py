from sqlalchemy import Column, Integer, Date, Text, DateTime, Boolean, String, ForeignKey
from datetime import datetime
from src.db.base import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type = Column(String, nullable=False)  # casual, sick, annual, unpaid
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    half_day = Column(Boolean, default=False)
    half_day_type = Column(String, nullable=True)  # first_half/second_half
    status = Column(String, nullable=False, default="pending")  # pending/approved/rejected
    approver_level = Column(Integer, default=1)  # 1=manager,2=hr,3=cfo etc
    created_at = Column(DateTime, default=datetime.utcnow)
