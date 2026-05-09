from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.auth_service import verify_token
from app.services.challenges_service import (
    create_challenge,
    get_challenges_by_user,
    get_challenge_by_id,
    update_challenge,
    delete_challenge,
    generate_personalized_challenges
)
from app.models.challenges import Challenge, ChallengeCreate, ChallengeUpdate

router = APIRouter()


@router.post("/", response_model=Challenge)
async def create_new_challenge(
    challenge_data: ChallengeCreate,
    user_id: str = Depends(verify_token)
):
    """Crear un nuevo desafío"""
    try:
        challenge = create_challenge(int(user_id), challenge_data)
        return challenge
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Challenge])
async def get_user_challenges(user_id: str = Depends(verify_token)):
    """Obtener todos los desafíos del usuario"""
    try:
        challenges = get_challenges_by_user(int(user_id))
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{challenge_id}", response_model=Challenge)
async def get_single_challenge(
    challenge_id: int,
    user_id: str = Depends(verify_token)
):
    """Obtener un desafío específico"""
    challenge = get_challenge_by_id(challenge_id, int(user_id))
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafío no encontrado")
    return challenge


@router.put("/{challenge_id}", response_model=Challenge)
async def update_existing_challenge(
    challenge_id: int,
    challenge_data: ChallengeUpdate,
    user_id: str = Depends(verify_token)
):
    """Actualizar un desafío"""
    challenge = update_challenge(challenge_id, int(user_id), challenge_data)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafío no encontrado")
    return challenge


@router.delete("/{challenge_id}")
async def delete_existing_challenge(
    challenge_id: int,
    user_id: str = Depends(verify_token)
):
    """Eliminar un desafío"""
    deleted = delete_challenge(challenge_id, int(user_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Desafío no encontrado")
    return {"message": "Desafío eliminado exitosamente"}


@router.post("/generate-personalized", response_model=List[Challenge])
async def generate_personalized_challenges_endpoint(
    user_id: str = Depends(verify_token)
):
    """Generar retos personalizados basados en el perfil del usuario"""
    try:
        challenges = generate_personalized_challenges(int(user_id))
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))