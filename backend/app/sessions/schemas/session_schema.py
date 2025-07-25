from pydantic import BaseModel
from typing import List

class SessionResponse(BaseModel):
    id: str
    device: str | None = None
    ip: str | None = None
    mac: str | None = None
    login_at: str | None = None
    logout_at: str | None = None
    is_active: bool

class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]

class SessionRevokeRequest(BaseModel):
    session_id: str

__all__ = ["SessionResponse", "SessionListResponse", "SessionRevokeRequest"] 