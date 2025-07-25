from pydantic import BaseModel, EmailStr, constr

class ProfileResponse(BaseModel):
    id: str
    email: EmailStr
    phone: constr(pattern=r"^\+?[1-9]\d{1,14}$")
    name: str | None = None
    profile_pic: str | None = None
    is_email_verified: bool
    is_phone_verified: bool
    is_2fa_enabled: bool

class ProfileUpdate(BaseModel):
    name: str | None = None
    profile_pic: str | None = None
    email: EmailStr | None = None
    phone: constr(pattern=r"^\+?[1-9]\d{1,14}$") | None = None

__all__ = ["ProfileResponse", "ProfileUpdate"] 