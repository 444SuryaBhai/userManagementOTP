from app.models.user import User
from app.db.session import get_db
from app.shared.otp_utils import generate_otp
from app.shared.email_utils import send_email_async
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

settings = get_settings()

async def register_user(data, db):
    # Check for existing email/phone
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if existing_user.is_email_verified:
            raise HTTPException(status_code=400, detail="Email already registered and verified")
        # Resend OTPs for unverified user
        user = existing_user
        user.name = data.name
        user.phone = data.phone
        user.profile_pic = data.profile_pic
        user.is_2fa_enabled = data.enable_2fa
        await db.commit()
        await db.refresh(user)
    else:
        result = await db.execute(select(User).where(User.phone == data.phone))
        existing_phone_user = result.scalar_one_or_none()
        if existing_phone_user:
            if existing_phone_user.is_phone_verified:
                raise HTTPException(status_code=400, detail="Phone already registered and verified")
            # Resend OTPs for unverified user
            user = existing_phone_user
            user.name = data.name
            user.email = data.email
            user.profile_pic = data.profile_pic
            user.is_2fa_enabled = data.enable_2fa
            await db.commit()
            await db.refresh(user)
        else:
            # Create user
            user = User(
                email=data.email,
                phone=data.phone,
                name=data.name,
                profile_pic=data.profile_pic,
                is_2fa_enabled=data.enable_2fa
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
    # Generate OTPs
    email_otp = await generate_otp(str(user.id), otp_type="email")
    phone_otp = await generate_otp(str(user.id), otp_type="phone")
    await send_email_async(
        to=user.email,
        subject="Verify your email",
        body=f"Your email verification OTP is {email_otp}",
        html=f"<p>Your email verification OTP is <b>{email_otp}</b></p>"
    )
    # For phone, just log OTP (simulate SMS send)
    if settings.ENV == "development":
        autofill = {"email_otp": email_otp, "phone_otp": phone_otp}
    else:
        autofill = None
    return str(user.id), autofill 