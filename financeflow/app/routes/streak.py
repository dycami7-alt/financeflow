from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from datetime import datetime
from app.services.streak_service import (
    get_streak,
    get_or_create_streak,
    update_streak,
    track_daily_activity,
    reset_streak,
    update_streak_manual
)
from app.models.streak import StreakUpdate
from app.services.auth_service import verify_token

router = APIRouter()

@router.get("/")
async def get_user_streak(user_id: str = Depends(verify_token)):
    """
    Obtiene la racha del usuario actual
    """
    try:
        streak = get_or_create_streak(int(user_id))
        return {
            "success": True,
            "data": streak
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update")
async def update_user_streak(user_id: str = Depends(verify_token)):
    """
    Actualiza la racha del usuario cuando completa una acción.
    Se llama cada vez que el usuario realiza una acción importante.
    """
    try:
        streak = update_streak(int(user_id))
        return {
            "success": True,
            "message": "Racha actualizada",
            "data": streak
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/track")
async def track_daily_interaction(user_id: str = Depends(verify_token)):
    """
    Registra la interacción diaria del usuario.
    Retorna si la racha se incrementó, se mantuvo o se reinició.
    """
    try:
        result = track_daily_activity(int(user_id))
        return {
            "success": True,
            "message": "Interacción diaria registrada",
            "status": result["status"],
            "days_since_last_activity": result["days_since_last_activity"],
            "data": result["streak"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
async def update_streak_manual_endpoint(
    update_data: StreakUpdate,
    user_id: str = Depends(verify_token)
):
    """
    Actualiza manualmente la racha del usuario
    """
    try:
        streak = update_streak_manual(int(user_id), update_data)
        if not streak:
            raise HTTPException(status_code=404, detail="Racha no encontrada")
        return {
            "success": True,
            "message": "Racha actualizada",
            "data": streak
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_user_streak(user_id: str = Depends(verify_token)):
    """
    Reinicia la racha del usuario
    """
    try:
        streak = reset_streak(int(user_id))
        return {
            "success": True,
            "message": "Racha reiniciada",
            "data": streak
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_streak_stats(user_id: str = Depends(verify_token)):
    """
    Obtiene estadísticas detalladas de la racha del usuario
    """
    try:
        streak = get_or_create_streak(int(user_id))

        # Calcular estadísticas adicionales
        stats = {
            "current_streak": streak.current_streak,
            "best_streak": streak.best_streak,
            "last_activity_date": streak.last_activity_date,
            "is_active_today": False,
            "days_since_last_activity": None
        }

        if streak.last_activity_date:
            last_date = datetime.fromisoformat(streak.last_activity_date).date()
            today = datetime.now().date()
            days_diff = (today - last_date).days

            stats["is_active_today"] = days_diff == 0
            stats["days_since_last_activity"] = days_diff

        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))