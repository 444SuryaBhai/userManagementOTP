from pydantic import BaseModel

class TwoFASetupResponse(BaseModel):
    secret: str
    qr_code_url: str

class TwoFAVerifyRequest(BaseModel):
    user_id: str
    token: str

class TwoFAStatusResponse(BaseModel):
    is_2fa_enabled: bool

__all__ = ["TwoFASetupResponse", "TwoFAVerifyRequest", "TwoFAStatusResponse"] 