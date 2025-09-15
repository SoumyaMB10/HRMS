from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from src.db.base import Base

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    mandatory = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PolicyAcknowledgement(Base):
    __tablename__ = "policy_acknowledgements"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    acknowledged_at = Column(DateTime, default=datetime.utcnow)
