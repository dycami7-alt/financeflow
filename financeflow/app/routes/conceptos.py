from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_conceptos():
    """Obtiene los conceptos financieros"""
    return {"mensaje": "Conceptos financieros"}
