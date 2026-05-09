from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator

from app.services.openia_service import ClaudeAPIError, send_claude_message
from app.services.rate_limiter import check_rate_limit
from app.services.chat_service import save_message, get_chat_history, clear_chat_history
from app.services.auth_service import verify_token

router = APIRouter()


class UserMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

    @validator("message")
    def strip_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El mensaje no puede estar vacío.")
        return value


@router.get("/historial")
async def get_chat_historial(user_id: str = Depends(verify_token)):
    """Obtiene el historial de chat del usuario"""
    try:
        history = get_chat_history(int(user_id))
        return {"historial": [msg.dict() for msg in history]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(exc)}")


@router.delete("/historial")
async def clear_chat_historial(user_id: str = Depends(verify_token)):
    """Limpia el historial de chat del usuario"""
    try:
        cleared = clear_chat_history(int(user_id))
        return {"message": "Historial limpiado exitosamente" if cleared else "No había historial que limpiar"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al limpiar historial: {str(exc)}")


@router.post("/mensaje")
async def send_message(
    payload: UserMessage,
    user_id: str = Depends(verify_token),
    _rate_limit: None = Depends(check_rate_limit),
):
    """Envía un mensaje al chat y recibe la respuesta de Claude"""
    try:
        # Guardar mensaje del usuario
        save_message(int(user_id), "user", payload.message)

        # Obtener historial de chat (últimos 20 mensajes para mantener contexto razonable)
        history = get_chat_history(int(user_id), limit=20)

        # Convertir a formato para Claude
        claude_history = [{"role": msg.role, "content": msg.content} for msg in history]

        # Enviar a Claude con historial
        respuesta = await send_claude_message(payload.message, claude_history)

        # Guardar respuesta de Claude
        save_message(int(user_id), "assistant", respuesta)

        return {"mensaje_usuario": payload.message, "respuesta_claude": respuesta}
    except ClaudeAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(exc)}")
