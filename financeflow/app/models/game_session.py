from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class GameSession(BaseModel):
    id: Optional[int] = None
    user_id: int
    game_type: str
    score: int
    decisions: List[Dict[str, Any]]
    completed_at: Optional[str] = None


class GameSessionCreate(BaseModel):
    user_id: int
    game_type: str = "financial"
    score: int
    decisions: List[Dict[str, Any]]
