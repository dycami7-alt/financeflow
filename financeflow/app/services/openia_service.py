import httpx
from typing import List, Dict, Any

from app.config import (
    CLAUDE_API_KEY,
    CLAUDE_API_URL,
    CLAUDE_MODEL,
    CLAUDE_MAX_TOKENS,
)


class ClaudeAPIError(Exception):
    """Error al comunicarse con Claude API."""


async def send_claude_message(message: str, history: List[Dict[str, str]] = None) -> str:
    if not CLAUDE_API_KEY:
        raise ValueError("CLAUDE_API_KEY no está configurada en el entorno.")

    # Preparar mensajes para Claude
    messages = []
    if history:
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Agregar el mensaje actual
    messages.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": CLAUDE_MODEL,
        "messages": messages,
        "max_tokens": CLAUDE_MAX_TOKENS,
        "temperature": 0.7,
        "top_p": 1.0,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",  # Para usar el formato de messages
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        raise ClaudeAPIError(
            f"Claude API respondió con {exc.response.status_code}: {exc.response.text}"
        ) from exc
    except httpx.RequestError as exc:
        raise ClaudeAPIError("Error de conexión con Claude API.") from exc

    if not isinstance(data, dict) or "content" not in data:
        raise ClaudeAPIError("Respuesta inesperada de Claude API.")

    content = data["content"]
    if not isinstance(content, list) or not content:
        raise ClaudeAPIError("Claude API devolvió datos no válidos.")

    # Extraer el texto de la respuesta
    completion = ""
    for block in content:
        if block.get("type") == "text":
            completion += block.get("text", "")

    return completion.strip()

    return completion.strip()
