from pydantic import BaseModel

class SettingsResponse(BaseModel):
    is_2fa_enabled: bool
    account_status: str  # active, deactivated, deleted

class SettingsUpdate(BaseModel):
    is_2fa_enabled: bool | None = None
    account_status: str | None = None  # active, deactivated, deleted

__all__ = ["SettingsResponse", "SettingsUpdate"] 