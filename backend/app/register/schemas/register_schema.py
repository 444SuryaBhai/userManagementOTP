from pydantic import BaseModel, EmailStr, constr

class RegisterInput(BaseModel):
    email: EmailStr
    phone: constr(pattern=r"^\+?[1-9]\d{1,14}$")
    name: str | None = None
    profile_pic: str | None = None
    enable_2fa: bool = False

class RegisterResponse(BaseModel):
    user_id: str
    message: str

__all__ = ["RegisterInput", "RegisterResponse"] 