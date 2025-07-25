from fastapi import APIRouter, Depends, status
from app.register.schemas.otp_schema import RegisterOTPVerify, RegisterOTPResponse
from app.register.services.otp_register_service import verify_register_otp
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/register/otp", tags=["Register OTP"])

@router.post("/verify", response_model=RegisterOTPResponse)
async def verify_register_otp_route(data: RegisterOTPVerify, db: AsyncSession = Depends(get_db)):
    await verify_register_otp(data.user_id, data.otp, data.type, db)
    return RegisterOTPResponse(message="OTP verified successfully.") 