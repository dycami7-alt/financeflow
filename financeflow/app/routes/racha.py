from fastapi import APIRouter, HTTPException
from app.services import racha_service

router = APIRouter()

@router.get("/stats/{user_id}")
async def get_streak_stats(user_id: str):
    """
    Obtiene las estadísticas de racha del usuario
    """
    try:
        stats = racha_service.get_racha_stats(user_id)
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update/{user_id}")
async def update_streak(user_id: str):
    """
    Actualiza la racha del usuario cuando completa una acción.
    Se llama cada vez que el usuario realiza una acción importante.
    """
    try:
        racha = racha_service.update_racha(user_id)
        return {
            "success": True,
            "message": "Racha actualizada",
            "data": racha.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_racha(user_id: str):
    """
    Obtiene la información actual de racha del usuario
    """
    try:
        racha = racha_service.get_racha(user_id)
        return {
            "success": True,
            "data": racha
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset/{user_id}")
async def reset_streak(user_id: str):
    """
    Reinicia la racha actual del usuario (mantiene el mejor record)
    """
    try:
        racha = racha_service.reset_racha(user_id)
        return {
            "success": True,
            "message": "Racha reiniciada",
            "data": racha
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
