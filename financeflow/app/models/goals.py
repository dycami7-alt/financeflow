from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Goal(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    target_amount: float
    current_amount: float = 0.0
    deadline: str  # ISO format date string
    status: str = "active"
    created_at: Optional[str] = None


class GoalCreate(BaseModel):
    title: str
    target_amount: float
    deadline: str
    status: Optional[str] = "active"


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[str] = None
    status: Optional[str] = None