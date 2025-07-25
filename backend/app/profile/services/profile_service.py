from app.models.user import User
from app.models.soft_deleted_contacts import SoftDeletedContact
from app.shared.otp_utils import generate_otp
from app.shared.email_utils import send_email_async
from app.db.session import get_db
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

settings = get_settings()

async def get_profile(user_id: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def update_profile(user_id: str, data, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update name/profile_pic
    if data.name is not None:
        user.name = data.name
    if data.profile_pic is not None:
        user.profile_pic = data.profile_pic
    # Email change
    if data.email and data.email != user.email:
        # Soft delete old email
        db.add(SoftDeletedContact(user_id=user.id, contact_type="email", value=user.email))
        # Send OTP to old and new email
        old_otp = await generate_otp(str(user.id), otp_type="email")
        await send_email_async(
            to=user.email,
            subject="Email Change Verification (Old Email)",
            body=f"Your OTP for email change is {old_otp}",
            html=f"<p>Your OTP for email change is <b>{old_otp}</b></p>"
        )
        new_otp = await generate_otp(str(user.id), otp_type="email_new")
        await send_email_async(
            to=data.email,
            subject="Email Change Verification (New Email)",
            body=f"Your OTP for email change is {new_otp}",
            html=f"<p>Your OTP for email change is <b>{new_otp}</b></p>"
        )
        user.email = data.email
        user.is_email_verified = False
    # Phone change
    if data.phone and data.phone != user.phone:
        db.add(SoftDeletedContact(user_id=user.id, contact_type="phone", value=user.phone))
        # Send OTP to old phone (simulate)
        old_otp = await generate_otp(str(user.id), otp_type="phone")
        # Send OTP to old email as well
        email_otp = await generate_otp(str(user.id), otp_type="email")
        await send_email_async(
            to=user.email,
            subject="Phone Change Verification (Email)",
            body=f"Your OTP for phone change is {email_otp}",
            html=f"<p>Your OTP for phone change is <b>{email_otp}</b></p>"
        )
        # Send OTP to new phone (simulate)
        new_otp = await generate_otp(str(user.id), otp_type="phone_new")
        user.phone = data.phone
        user.is_phone_verified = False
    await db.commit()
    await db.refresh(user)
    return user 