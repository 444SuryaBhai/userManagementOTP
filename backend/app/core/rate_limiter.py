from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.database import redis
from app.config.config import get_settings
import time
from starlette.responses import Response

settings = get_settings()

RATE_LIMIT = settings.RATE_LIMIT
RATE_LIMIT_WINDOW = settings.RATE_LIMIT_WINDOW

async def check_rate_limit(key: str, limit: int = RATE_LIMIT, window: int = RATE_LIMIT_WINDOW):
    now = int(time.time())
    window_start = now - window
    count = await redis.zcount(key, window_start, now)
    if count >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    await redis.zadd(key, {str(now): now})
    await redis.expire(key, window)

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("X-User-Id")
        ip = request.client.host
        key = f"rate:{user_id or ip}"
        try:
            await check_rate_limit(key)
        except HTTPException as e:
            return Response(content=e.detail, status_code=e.status_code)
        response = await call_next(request)
        return response 