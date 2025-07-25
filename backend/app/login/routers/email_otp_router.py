from fastapi import APIRouter, Depends, status
from app.login.schemas.login_input import EmailLoginInput
from app.login.schemas.otp_schema import OTPVerify, OTPResponse
from app.login.schemas.token_schema import TokenResponse
from app.login.services.email_otp_service import send_email_otp, verify_email_otp
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import get_settings

router = APIRouter(prefix="/login/email-otp", tags=["Login - Email OTP"])
settings = get_settings()

@router.post("/request", response_model=OTPResponse)
async def request_email_otp(data: EmailLoginInput, db: AsyncSession = Depends(get_db)):
    autofill_otp, user_id = await send_email_otp(data.email, db)
    return OTPResponse(message="OTP sent to email", autofill_otp=autofill_otp, user_id=user_id)

@router.post("/verify", response_model=TokenResponse)
async def verify_email_otp_route(data: OTPVerify, db: AsyncSession = Depends(get_db)):
    access_token, refresh_token = await verify_email_otp(data.user_id, data.otp, db)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    ) 