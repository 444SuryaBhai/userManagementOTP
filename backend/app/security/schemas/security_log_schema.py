from pydantic import BaseModel
from typing import List

class SecurityLogResponse(BaseModel):
    id: str
    action: str
    ip: str | None = None
    device: str | None = None
    created_at: str

class SecurityLogListResponse(BaseModel):
    logs: List[SecurityLogResponse]

__all__ = ["SecurityLogResponse", "SecurityLogListResponse"] 