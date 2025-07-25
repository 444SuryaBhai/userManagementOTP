from datetime import datetime, timedelta
from app.db.database import redis
from app.config.config import get_settings

settings = get_settings()
IDLE_TIMEOUT_MINUTES = settings.SESSION_EXPIRE_MINUTES

async def set_user_activity(user_id: str):
    now = datetime.utcnow().isoformat()
    await redis.set(f"user:activity:{user_id}", now)

async def get_user_last_activity(user_id: str) -> datetime:
    last = await redis.get(f"user:activity:{user_id}")
    if last:
        return datetime.fromisoformat(last)
    return None

async def is_user_idle(user_id: str) -> bool:
    last = await get_user_last_activity(user_id)
    if not last:
        return True
    return datetime.utcnow() - last > timedelta(minutes=IDLE_TIMEOUT_MINUTES)

async def logout_if_idle(user_id: str):
    if await is_user_idle(user_id):
        # Invalidate session/token logic here
        await redis.delete(f"user:session:{user_id}")
        return True
    return False 