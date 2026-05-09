from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.perfil_service import calculate_profile, save_profile, get_user_profile

router = APIRouter()

@router.get("/{user_id}")
async def get_perfil(user_id: int):
    """Obtiene el perfil del usuario"""
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile.to_dict()

@router.put("/")
async def update_perfil(data: dict):
    """Actualiza el perfil del usuario"""
    return {"actualizado": data}

@router.post("/quiz")
async def submit_quiz_answers(data: Dict[str, Any]):
    """Recibe las respuestas del perfilador, calcula y guarda el perfil"""
    user_id = data.get("user_id")
    answers = data.get("answers", [])

    if not user_id or not answers:
        raise HTTPException(status_code=400, detail="user_id y answers son requeridos")

    if not isinstance(answers, list) or len(answers) != 6:  # Asumiendo 6 preguntas
        raise HTTPException(status_code=400, detail="Debe proporcionar exactamente 6 respuestas")

    # Calcular perfil
    profile_data = calculate_profile(answers)

    # Guardar en BD
    profile_id = save_profile(user_id, profile_data, answers)

    # Retornar resultado
    return {
        "profile_id": profile_id,
        "profile": profile_data
    }
