from fastapi import APIRouter, Depends, status
from app.login.schemas.login_input import OAuthLoginInput
from app.login.schemas.token_schema import TokenResponse
from app.login.services.oauth_service import oauth_login
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.config.config import get_settings

router = APIRouter(prefix="/login/oauth", tags=["Login - OAuth"])
settings = get_settings()

@router.post("/", response_model=TokenResponse)
async def oauth_login_route(data: OAuthLoginInput, db: AsyncSession = Depends(get_db)):
    access_token, refresh_token, user = await oauth_login(data.provider, data.code, data.redirect_uri, db)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    ) 