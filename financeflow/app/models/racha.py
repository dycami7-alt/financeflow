from datetime import datetime
from typing import Optional

class RachaData:
    """Modelo para gestionar las rachas del usuario"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_streak = 0
        self.best_streak = 0
        self.last_action_date = None
        self.total_actions = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "last_action_date": self.last_action_date,
            "total_actions": self.total_actions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
