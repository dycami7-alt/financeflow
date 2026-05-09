from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Challenge(BaseModel):
    id: Optional[int] = None
    user_id: int
    challenge_type: str
    reward: str
    created_at: Optional[str] = None


class ChallengeCreate(BaseModel):
    challenge_type: str
    reward: str


class ChallengeUpdate(BaseModel):
    challenge_type: Optional[str] = None
    reward: Optional[str] = None