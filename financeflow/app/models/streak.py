from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Streak(BaseModel):
    id: Optional[int] = None
    user_id: int
    current_streak: int = 0
    best_streak: int = 0
    last_activity_date: Optional[str] = None  # ISO format date string
    created_at: Optional[str] = None


class StreakUpdate(BaseModel):
    current_streak: Optional[int] = None
    best_streak: Optional[int] = None
    last_activity_date: Optional[str] = None