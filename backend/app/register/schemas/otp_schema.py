from pydantic import BaseModel, constr

class RegisterOTPVerify(BaseModel):
    user_id: str
    otp: constr(min_length=6, max_length=6)
    type: str  # email or phone

class RegisterOTPResponse(BaseModel):
    message: str
    autofill_otp: str | None = None

__all__ = ["RegisterOTPVerify", "RegisterOTPResponse"] 