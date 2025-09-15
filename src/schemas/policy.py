from pydantic import BaseModel

class PolicyAcknowledge(BaseModel):
    user_id: int
    policy_id: int

class CalendarItem(BaseModel):
    date: str
    reason: str
