from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from app.db.database import redis
from app.config.config import get_settings

settings = get_settings()

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
        if not session_id:
            return await call_next(request)
        session_key = f"session:{session_id}"
        session_data = await redis.get(session_key)
        if not session_data:
            # Optionally, clear the cookie if session is invalid
            response = await call_next(request)
            response.delete_cookie(settings.SESSION_COOKIE_NAME)
            return response
        request.state.session = session_data
        response = await call_next(request)
        return response 