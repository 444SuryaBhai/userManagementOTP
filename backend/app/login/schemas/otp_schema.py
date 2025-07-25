from pydantic import BaseModel, EmailStr, constr

class OTPRequest(BaseModel):
    email: EmailStr | None = None
    phone: constr(pattern=r"^\+?[1-9]\d{1,14}$") | None = None
    type: str  # email or phone

class OTPVerify(BaseModel):
    user_id: str
    otp: constr(min_length=6, max_length=6)
    type: str  # email or phone

class OTPResponse(BaseModel):
    message: str
    autofill_otp: str | None = None  # For dev autofill
    user_id: str | None = None  # For frontend OTP verification

__all__ = ["OTPRequest", "OTPVerify", "OTPResponse"] 