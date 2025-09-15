from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.user import User
from src.models.leave import LeaveRequest

def list_team_leaves(db: Session, manager_id: int):
    try:
        reports = db.query(User).filter(User.manager_id == manager_id).all()
        ids = [r.id for r in reports]
        leaves = db.query(LeaveRequest).filter(LeaveRequest.user_id.in_(ids)).order_by(LeaveRequest.created_at.desc()).all()
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def approve_leave(db: Session, leave_id: int, approver_id: int):
    try:
        leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
        if not leave:
            raise HTTPException(status_code=404, detail="Leave not found")
        if leave.status != "pending":
            raise HTTPException(status_code=400, detail="Leave already processed")
        approver = db.query(User).filter(User.id == approver_id).first()
        if not approver:
            raise HTTPException(status_code=404, detail="Approver not found")

        # Level 1 = Manager approval
        if leave.approver_level == 1:
            requester = db.query(User).filter(User.id == leave.user_id).first()
            is_manager = requester and requester.manager_id == approver.id
            if not is_manager and approver.role not in ("hr", "hr_manager", "cfo", "admin"):
                raise HTTPException(status_code=403, detail="Not authorized at level 1")
            leave.approver_level = 2
        elif leave.approver_level == 2:
            if approver.role not in ("hr", "hr_manager", "cfo", "admin"):
                raise HTTPException(status_code=403, detail="Not authorized at level 2")
            leave.status = "approved"
        else:
            raise HTTPException(status_code=400, detail="Invalid approver level")
        db.commit()
        db.refresh(leave)
        return leave
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Approve leave failed: {str(e)}")

def reject_leave(db: Session, leave_id: int, approver_id: int):
    try:
        leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
        if not leave:
            raise HTTPException(status_code=404, detail="Leave not found")
        leave.status = "rejected"
        db.commit()
        db.refresh(leave)
        return leave
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reject leave failed: {str(e)}")
