from fastapi import Response, Request
from app.config.config import get_settings

settings = get_settings()

COOKIE_SETTINGS = {
    "httponly": True,
    "samesite": "lax",
    "secure": False if settings.ENV == "development" else True,
    "path": "/",
}


def set_cookie(response: Response, key: str, value: str, max_age: int = None):
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        **COOKIE_SETTINGS
    )

def get_cookie(request: Request, key: str):
    return request.cookies.get(key)

def delete_cookie(response: Response, key: str):
    response.delete_cookie(key=key, path="/") 