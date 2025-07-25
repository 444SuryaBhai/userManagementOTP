from app.core.jwt import create_access_token, create_refresh_token
from app.models.user import User
from app.models.token import Token
from app.db.session import get_db
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime, timedelta
import uuid
from authlib.integrations.httpx_client import AsyncOAuth2Client

settings = get_settings()

OAUTH_PROVIDERS = {
    "google": {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
    },
    "github": {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
    },
    "linkedin": {
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
        "userinfo_url": "https://api.linkedin.com/v2/me",
    },
    "microsoft": {
        "client_id": settings.MICROSOFT_CLIENT_ID,
        "client_secret": settings.MICROSOFT_CLIENT_SECRET,
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/v1.0/me",
    },
}

async def oauth_login(provider: str, code: str, redirect_uri: str, db):
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    conf = OAUTH_PROVIDERS[provider]
    async with AsyncOAuth2Client(
        client_id=conf["client_id"],
        client_secret=conf["client_secret"],
        redirect_uri=redirect_uri,
    ) as client:
        # Exchange code for token
        token = await client.fetch_token(
            conf["token_url"],
            code=code,
            grant_type="authorization_code",
            client_secret=conf["client_secret"],
        )
        # Fetch user info
        if provider == "google":
            resp = await client.get(conf["userinfo_url"])
            info = resp.json()
            email = info.get("email")
            name = info.get("name")
            picture = info.get("picture")
        elif provider == "github":
            resp = await client.get(conf["userinfo_url"])
            info = resp.json()
            email = info.get("email")
            name = info.get("name")
            picture = info.get("avatar_url")
        elif provider == "linkedin":
            resp = await client.get(conf["userinfo_url"])
            info = resp.json()
            email = None  # LinkedIn requires extra call for email
            name = info.get("localizedFirstName")
            picture = None
        elif provider == "microsoft":
            resp = await client.get(conf["userinfo_url"])
            info = resp.json()
            email = info.get("userPrincipalName")
            name = info.get("displayName")
            picture = None
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")
        if not email:
            raise HTTPException(status_code=400, detail="Email not found from OAuth provider")
        # Find or create user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            user = User(email=email, name=name, profile_pic=picture, is_email_verified=True)
            db.add(user)
            await db.commit()
            await db.refresh(user)
        # Create tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db_token = Token(
            user_id=user.id,
            token=refresh_token,
            type="refresh",
            expires_at=expires_at
        )
        db.add(db_token)
        await db.commit()
        return access_token, refresh_token, user 