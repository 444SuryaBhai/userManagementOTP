from app.models.user import User
from app.db.session import get_db
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

settings = get_settings()

VALID_STATUSES = {"active", "deactivated", "deleted"}

async def get_settings_service(user_id: str, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.is_2fa_enabled, getattr(user, "account_status", "active")

async def update_settings_service(user_id: str, data, db):
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.is_2fa_enabled is not None:
        user.is_2fa_enabled = data.is_2fa_enabled
    if data.account_status:
        if data.account_status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid account status")
        user.account_status = data.account_status
        if data.account_status == "deleted":
            user.is_active = False  # Soft delete
    await db.commit()
    await db.refresh(user)
    return user 