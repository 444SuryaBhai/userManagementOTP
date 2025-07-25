from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from app.core.jwt import decode_token
from app.config.config import get_settings

settings = get_settings()

PUBLIC_PATHS = ["/health", "/login", "/register", "/docs", "/openapi.json"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)
        token = request.cookies.get("access_token")
        # Also check Authorization header for Bearer token
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1]
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        request.state.user = payload
        return await call_next(request) 