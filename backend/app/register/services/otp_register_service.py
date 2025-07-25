from app.models.user import User
from app.shared.otp_utils import verify_otp
from app.db.session import get_db
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

async def verify_register_otp(user_id: str, otp: str, otp_type: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not await verify_otp(user_id, otp, otp_type=otp_type):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if otp_type == "email" and not user.is_email_verified:
        user.is_email_verified = True
        await db.commit()
    if otp_type == "phone" and not user.is_phone_verified:
        user.is_phone_verified = True
        await db.commit()
    return True 