from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator

from app.services.openia_service import ClaudeAPIError, send_claude_message
from app.services.rate_limiter import check_rate_limit

router = APIRouter()


class UserMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

    @validator("message")
    def strip_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El mensaje no puede estar vacío.")
        return value


@router.get("/")
async def get_chat():
    """Obtiene el chat"""
    return {"mensaje": "Chat endpoint"}


@router.post("/mensaje")
async def send_message(
    payload: UserMessage,
    _rate_limit: None = Depends(check_rate_limit),
):
    """Envía un mensaje al chat y recibe la respuesta de Claude"""
    try:
        respuesta = await send_claude_message(payload.message)
        return {"mensaje_usuario": payload.message, "respuesta_claude": respuesta}
    except ClaudeAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar el mensaje.",
        )
