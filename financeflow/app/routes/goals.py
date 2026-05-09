from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.auth_service import verify_token
from app.services.goals_service import (
    create_goal,
    get_goals_by_user,
    get_goal_by_id,
    update_goal,
    delete_goal,
    complete_goal
)
from app.models.goals import Goal, GoalCreate, GoalUpdate

router = APIRouter()


@router.post("/", response_model=Goal)
async def create_new_goal(
    goal_data: GoalCreate,
    user_id: str = Depends(verify_token)
):
    """Crear una nueva meta financiera"""
    try:
        goal = create_goal(int(user_id), goal_data)
        return goal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Goal])
async def get_user_goals(user_id: str = Depends(verify_token)):
    """Obtener todas las metas del usuario"""
    try:
        goals = get_goals_by_user(int(user_id))
        return goals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{goal_id}", response_model=Goal)
async def get_single_goal(
    goal_id: int,
    user_id: str = Depends(verify_token)
):
    """Obtener una meta específica"""
    goal = get_goal_by_id(goal_id, int(user_id))
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return goal


@router.put("/{goal_id}", response_model=Goal)
async def update_existing_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    user_id: str = Depends(verify_token)
):
    """Actualizar una meta"""
    goal = update_goal(goal_id, int(user_id), goal_data)
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return goal


@router.delete("/{goal_id}")
async def delete_existing_goal(
    goal_id: int,
    user_id: str = Depends(verify_token)
):
    """Eliminar una meta"""
    deleted = delete_goal(goal_id, int(user_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return {"message": "Meta eliminada exitosamente"}


@router.post("/{goal_id}/complete", response_model=Goal)
async def complete_existing_goal(
    goal_id: int,
    user_id: str = Depends(verify_token)
):
    """Marcar una meta como completada"""
    goal = complete_goal(goal_id, int(user_id))
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return goal