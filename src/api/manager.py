from fastapi import APIRouter, Depends, HTTPException
from src.deps import get_db, get_current_user
from src.services.manager_service import list_team_leaves

router = APIRouter(prefix="/api/manager", tags=["manager"])

@router.get("/team/leaves")
def api_team_leaves(db = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ("manager", "hr", "hr_manager", "admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    return list_team_leaves(db, current_user.id)
