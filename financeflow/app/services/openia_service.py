import httpx

from app.config import (
    CLAUDE_API_KEY,
    CLAUDE_API_URL,
    CLAUDE_MODEL,
    CLAUDE_MAX_TOKENS,
)


class ClaudeAPIError(Exception):
    """Error al comunicarse con Claude API."""


async def send_claude_message(message: str) -> str:
    if not CLAUDE_API_KEY:
        raise ValueError("CLAUDE_API_KEY no está configurada en el entorno.")

    payload = {
        "model": CLAUDE_MODEL,
        "prompt": f"\n\nHuman: {message}\n\nAssistant:",
        "max_tokens_to_sample": CLAUDE_MAX_TOKENS,
        "temperature": 0.7,
        "top_p": 1.0,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
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

    if not isinstance(data, dict) or "completion" not in data:
        raise ClaudeAPIError("Respuesta inesperada de Claude API.")

    completion = data["completion"]
    if not isinstance(completion, str):
        raise ClaudeAPIError("Claude API devolvió datos no válidos.")

    return completion.strip()
