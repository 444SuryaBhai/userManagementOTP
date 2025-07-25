from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Session
    SESSION_SECRET_KEY: str
    SESSION_COOKIE_NAME: str = "session"
    SESSION_EXPIRE_MINUTES: int = 60

    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str = "User Management"

    # OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    OAUTH_REDIRECT_URI: str

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Rate Limiting
    RATE_LIMIT: int = 10
    RATE_LIMIT_WINDOW: int = 60

    # Other
    ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 