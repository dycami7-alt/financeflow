from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    id: Optional[int] = None
    user_id: int
    role: str  # 'user' or 'assistant'
    content: str
    created_at: Optional[str] = None