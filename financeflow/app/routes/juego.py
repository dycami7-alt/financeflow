from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_juego():
    """Obtiene el juego"""
    return {"mensaje": "Juego endpoint"}

@router.post("/jugar")
async def play_game(action: str):
    """Realiza una acción en el juego"""
    return {"resultado": action}
