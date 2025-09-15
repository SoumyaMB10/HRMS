from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.db.base import Base

class RecruitmentRequest(Base):
    __tablename__ = "recruitment_requests"
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending/approved/rejected
    approver_level = Column(Integer, default=1)  # 1=manager,2=hr,3=cfo
    created_at = Column(DateTime, default=datetime.utcnow)
