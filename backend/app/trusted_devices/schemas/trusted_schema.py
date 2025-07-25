from pydantic import BaseModel
from typing import List

class TrustedDeviceResponse(BaseModel):
    id: str
    device_info: str | None = None
    ip: str | None = None
    mac: str | None = None
    added_at: str | None = None
    is_active: bool

class TrustedDeviceListResponse(BaseModel):
    devices: List[TrustedDeviceResponse]

class TrustedDeviceAddRequest(BaseModel):
    device_info: str | None = None
    ip: str | None = None
    mac: str | None = None

__all__ = ["TrustedDeviceResponse", "TrustedDeviceListResponse", "TrustedDeviceAddRequest"] 