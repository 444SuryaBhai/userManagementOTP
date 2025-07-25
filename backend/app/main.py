import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config.config import get_settings
from app.db.database import create_db_and_tables, redis
from app.middlewares.rate_limiter import RateLimiterMiddleware

# Import routers from all feature modules
from app.login.routers import email_otp_router, phone_otp_router, oauth_router
from app.register.routers import register_router, otp_verification_router
from app.profile.routers.profile_router import router as profile_router
from app.settings.routers.settings_router import router as settings_router
from app.sessions.routers.session_router import router as session_router
from app.security.routers.security_log_router import router as security_log_router
from app.twofa.routers.twofa_router import router as twofa_router
from app.trusted_devices.routers.trusted_router import router as trusted_router

settings = get_settings()

app = FastAPI(title="User Management API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#settings.ALLOWED_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

# Rate Limiter Middleware
app.add_middleware(RateLimiterMiddleware)

@app.on_event("startup")
async def on_startup():
    # Test Redis connection if using aioredis, fallback if not available
    if hasattr(redis, "ping"):
        try:
            await redis.ping()
        except Exception:
            from app.db.database import InMemoryAsyncCache
            globals()["redis"] = InMemoryAsyncCache()
    await create_db_and_tables()

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# Register all routers
app.include_router(email_otp_router)
app.include_router(phone_otp_router)
app.include_router(oauth_router)
app.include_router(register_router)
app.include_router(otp_verification_router)
app.include_router(profile_router)
app.include_router(settings_router)
app.include_router(session_router)
app.include_router(security_log_router)
app.include_router(twofa_router)
app.include_router(trusted_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 