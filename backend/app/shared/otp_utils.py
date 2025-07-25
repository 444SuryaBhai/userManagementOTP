import random
from app.shared.redis_utils import set_with_expiry, get, delete
from app.config.config import get_settings

settings = get_settings()
OTP_EXPIRE_SECONDS = 300  # 5 minutes

async def generate_otp(user_id: str, otp_type: str = "email") -> str:
    otp = str(random.randint(100000, 999999))
    key = f"otp:{otp_type}:{user_id}"
    await set_with_expiry(key, otp, OTP_EXPIRE_SECONDS)
    return otp

async def verify_otp(user_id: str, otp: str, otp_type: str = "email") -> bool:
    key = f"otp:{otp_type}:{user_id}"
    stored = await get(key)
    if stored and stored == otp:
        await delete(key)
        return True
    return False 