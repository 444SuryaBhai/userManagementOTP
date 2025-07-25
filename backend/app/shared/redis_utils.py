from app.db.database import redis

async def set_with_expiry(key: str, value: str, expire: int):
    await redis.set(key, value, ex=expire)

async def get(key: str):
    return await redis.get(key)

async def delete(key: str):
    await redis.delete(key)

async def incr(key: str):
    return await redis.incr(key)

async def exists(key: str):
    return await redis.exists(key)

async def get_or_set(key: str, value_fn, expire: int = None):
    val = await get(key)
    if val is not None:
        return val
    val = await value_fn()
    await set_with_expiry(key, val, expire or 60)
    return val 