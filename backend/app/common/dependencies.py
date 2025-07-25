from fastapi import Depends, Request, HTTPException, status
from app.db.session import get_db
from typing import Any

def get_current_user(request: Request) -> dict[str, Any]:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user 