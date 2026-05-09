from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.game_service import create_game_session, get_game_sessions_by_user

router = APIRouter()


class GameSessionCreate(BaseModel):
    user_id: int
    score: int
    decisions: List[Dict[str, Any]]
    game_type: str = "financial"


class GameSessionResponse(BaseModel):
    id: int
    user_id: int
    game_type: str
    score: int
    decisions: List[Dict[str, Any]]
    completed_at: str


@router.get("/")
async def get_juego():
    """Obtiene el juego"""
    return {"mensaje": "Juego endpoint"}


@router.post("/jugar")
async def play_game(action: str):
    """Realiza una acción en el juego"""
    return {"resultado": action}


@router.post("/session", response_model=GameSessionResponse)
async def register_game_session(session: GameSessionCreate):
    """Registra una sesión de juego completada con score, decisiones y fecha."""
    if session.score < 0:
        raise HTTPException(status_code=400, detail="El score debe ser un valor positivo")

    session_id = create_game_session(
        user_id=session.user_id,
        score=session.score,
        decisions=session.decisions,
        game_type=session.game_type,
    )
    return get_game_sessions_by_user(session.user_id)[-1]


@router.get("/sessions/{user_id}", response_model=List[GameSessionResponse])
async def list_user_sessions(
    user_id: int,
    min_score: Optional[int] = Query(None, ge=0),
    start_date: Optional[str] = Query(None, description="Fecha inicial ISO 8601"),
    end_date: Optional[str] = Query(None, description="Fecha final ISO 8601"),
):
    """Devuelve sesiones de juego registradas para un usuario con filtros opcionales."""
    return get_game_sessions_by_user(
        user_id=user_id,
        min_score=min_score,
        start_date=start_date,
        end_date=end_date,
    )
