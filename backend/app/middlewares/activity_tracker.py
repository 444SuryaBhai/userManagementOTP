from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.activity import set_user_activity
from app.config.config import get_settings

settings = get_settings()

PUBLIC_PATHS = ["/health", "/login", "/register", "/docs", "/openapi.json"]

class ActivityTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)
        user = getattr(request.state, "user", None)
        if user and "sub" in user:
            await set_user_activity(user["sub"])
        response = await call_next(request)
        return response 