import json
from datetime import datetime
from typing import List, Dict, Any


class Profile:
    """Modelo para el perfil financiero del usuario"""
    def __init__(self, user_id: int, profile_type: str, score: int, strengths: List[str], areas: List[str], savings_plan: str, risk_tolerance: str):
        self.id = None  # Se asigna al guardar en BD
        self.user_id = user_id
        self.profile_type = profile_type
        self.score = score
        self.strengths = strengths
        self.areas = areas
        self.savings_plan = savings_plan
        self.risk_tolerance = risk_tolerance
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "profile_type": self.profile_type,
            "score": self.score,
            "strengths": self.strengths,
            "areas": self.areas,
            "savings_plan": self.savings_plan,
            "risk_tolerance": self.risk_tolerance,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Profile':
        profile = Profile(
            user_id=data["user_id"],
            profile_type=data["profile_type"],
            score=data["score"],
            strengths=data["strengths"],
            areas=data["areas"],
            savings_plan=data["savings_plan"],
            risk_tolerance=data["risk_tolerance"]
        )
        profile.id = data.get("id")
        profile.created_at = datetime.fromisoformat(data["created_at"])
        return profile


class ProfileAnswer:
    """Modelo para las respuestas del perfilador"""
    def __init__(self, profile_id: int, question_id: int, answer_id: int, points: int, answer_type: str):
        self.id = None
        self.profile_id = profile_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.points = points
        self.answer_type = answer_type
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "question_id": self.question_id,
            "answer_id": self.answer_id,
            "points": self.points,
            "answer_type": self.answer_type,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ProfileAnswer':
        answer = ProfileAnswer(
            profile_id=data["profile_id"],
            question_id=data["question_id"],
            answer_id=data["answer_id"],
            points=data["points"],
            answer_type=data["answer_type"]
        )
        answer.id = data.get("id")
        answer.created_at = datetime.fromisoformat(data["created_at"])
        return answer