from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.policy import Policy, PolicyAcknowledgement

def create_policy(db: Session, title: str, document_url: str, mandatory: bool = False):
    try:
        p = Policy(title=title, document_url=document_url, mandatory=mandatory)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create policy failed: {str(e)}")

def acknowledge_policy(db: Session, user_id: int, policy_id: int):
    try:
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        ack = PolicyAcknowledgement(policy_id=policy_id, user_id=user_id)
        db.add(ack)
        db.commit()
        db.refresh(ack)
        return {"policy_id": policy_id, "user_id": user_id, "acknowledged": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Acknowledge failed: {str(e)}")
