from app.shared.otp_utils import generate_otp, verify_otp
from app.core.jwt import create_access_token, create_refresh_token
from app.models.user import User
from app.models.token import Token
from app.db.session import get_db
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import uuid
import logging

settings = get_settings()
logger = logging.getLogger("phone_otp_service")

async def send_phone_otp(phone: str, db):
    # Find user by phone
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = await generate_otp(str(user.id), otp_type="phone")
    # For now, just log the OTP (simulate SMS send)
    logger.info(f"[DEV] OTP for {phone}: {otp}")
    return (otp if settings.ENV == "development" else None), str(user.id)

async def verify_phone_otp(user_id: str, otp: str, db):
    # Find user
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not await verify_otp(user_id, otp, otp_type="phone"):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    # Mark phone as verified if not already
    if not user.is_phone_verified:
        user.is_phone_verified = True
        await db.commit()
    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    # Store refresh token in DB
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = Token(
        user_id=user.id,
        token=refresh_token,
        type="refresh",
        expires_at=expires_at
    )
    db.add(db_token)
    await db.commit()
    return access_token, refresh_token 