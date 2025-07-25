from app.models.user import User
from app.core.security import generate_2fa_secret, get_totp_uri, verify_totp
from app.db.session import get_db
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

async def setup_2fa(user_id: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    secret = generate_2fa_secret()
    qr_code_url = get_totp_uri(secret, user.email)
    user.twofa_secret = secret
    await db.commit()
    return secret, qr_code_url

async def verify_2fa(user_id: str, token: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user or not getattr(user, "twofa_secret", None):
        raise HTTPException(status_code=404, detail="2FA not setup for user")
    if not verify_totp(token, user.twofa_secret):
        raise HTTPException(status_code=400, detail="Invalid 2FA token")
    user.is_2fa_enabled = True
    await db.commit()
    return True

async def disable_2fa(user_id: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_2fa_enabled = False
    user.twofa_secret = None
    await db.commit()
    return True 