import asyncio
import time
from typing import Dict, List

from fastapi import HTTPException, Request

from app.config import CHAT_RATE_LIMIT_PER_MINUTE

_rate_limit_state: Dict[str, List[float]] = {}
_rate_limit_lock = asyncio.Lock()


async def check_rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "anonymous"
    now = time.time()
    window_start = now - 60

    async with _rate_limit_lock:
        request_times = _rate_limit_state.setdefault(client_ip, [])
        request_times[:] = [timestamp for timestamp in request_times if timestamp > window_start]

        if len(request_times) >= CHAT_RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail=(
                    f"Demasiadas solicitudes. Máximo {CHAT_RATE_LIMIT_PER_MINUTE} "
                    "peticiones por minuto."
                ),
                headers={"Retry-After": "60"},
            )

        request_times.append(now)
        _rate_limit_state[client_ip] = request_times
