from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from datetime import datetime
from src.db.base import Base

class PayrollRecord(Base):
    __tablename__ = "payroll_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period = Column(String, nullable=False)  # e.g., "2025-08"
    gross = Column(Float, nullable=False)
    deductions = Column(Float, nullable=True, default=0.0)
    net = Column(Float, nullable=False)
    payslip_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
