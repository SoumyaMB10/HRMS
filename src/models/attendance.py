from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from datetime import datetime
from src.db.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    total_hours = Column(Float, nullable=True)
    status = Column(String, nullable=True)  # online/offline
    exception = Column(String, nullable=True)  # late, early, missing_clockout, none
    created_at = Column(DateTime, default=datetime.utcnow)
