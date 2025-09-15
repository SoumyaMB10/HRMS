from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.db.base import Base

class ResignationRequest(Base):
    __tablename__ = "resignation_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notice_period_days = Column(Integer, nullable=True)
    reason = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending/accepted/rejected
    approver_level = Column(Integer, default=1)  # 1=manager,2=hr,3=cfo
    created_at = Column(DateTime, default=datetime.utcnow)
