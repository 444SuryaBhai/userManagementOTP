from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.config import get_settings
import aioredis
import asyncio

settings = get_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL, echo=settings.DEBUG, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class InMemoryAsyncCache:
    def __init__(self):
        self._store = {}
        self._lock = asyncio.Lock()

    async def set(self, key, value, ex=None):
        async with self._lock:
            self._store[key] = value
            # Optionally, handle expiry with a background task if needed

    async def get(self, key):
        async with self._lock:
            return self._store.get(key)

    async def delete(self, key):
        async with self._lock:
            if key in self._store:
                del self._store[key]

    async def incr(self, key):
        async with self._lock:
            value = int(self._store.get(key, 0)) + 1
            self._store[key] = value
            return value

    async def exists(self, key):
        async with self._lock:
            return key in self._store

    async def zcount(self, key, min_score, max_score):
        # For rate limiter: treat as sorted set of timestamps
        async with self._lock:
            zset = self._store.get(key, [])
            return len([v for v in zset if min_score <= v <= max_score])

    async def zadd(self, key, mapping):
        async with self._lock:
            zset = self._store.setdefault(key, [])
            for score in mapping.values():
                zset.append(score)

    async def expire(self, key, seconds):
        # Not implemented for in-memory fallback (could add with background task)
        pass

try:
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    # Test connection on startup
    async def test_redis():
        try:
            await redis.ping()
        except Exception:
            raise ImportError
    # Will be called on startup
except Exception:
    redis = InMemoryAsyncCache()

async def create_db_and_tables():
    from app.models import user, session, token, otp, trusted_device, security_log, soft_deleted_contacts
    async with engine.begin() as conn:
        await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(session.Base.metadata.create_all)
        await conn.run_sync(token.Base.metadata.create_all)
        await conn.run_sync(otp.Base.metadata.create_all)
        await conn.run_sync(trusted_device.Base.metadata.create_all)
        await conn.run_sync(security_log.Base.metadata.create_all)
        await conn.run_sync(soft_deleted_contacts.Base.metadata.create_all) 