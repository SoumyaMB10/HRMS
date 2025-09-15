from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    role: str
    password: str
    manager_id: Optional[int] = None  # optional reporting manager

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    manager_id: Optional[int] = None

    class Config:
        orm_mode = True
