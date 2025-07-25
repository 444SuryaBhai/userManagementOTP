from pydantic import BaseModel, EmailStr, constr

class EmailLoginInput(BaseModel):
    email: EmailStr

class PhoneLoginInput(BaseModel):
    phone: constr(pattern=r"^\+?[1-9]\d{1,14}$") 

class OAuthLoginInput(BaseModel):
    provider: str  # google, github, linkedin, microsoft
    code: str
    redirect_uri: str

__all__ = ["EmailLoginInput", "PhoneLoginInput", "OAuthLoginInput"] 