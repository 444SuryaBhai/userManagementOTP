from app.core.jwt import decode_token, create_access_token, create_refresh_token, is_refresh_token
from app.models.token import Token
from app.models.user import User
from app.db.session import get_db
from app.config.config import get_settings
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import uuid

settings = get_settings()

async def refresh_access_token(refresh_token: str, db):
    payload = decode_token(refresh_token)
    if not payload or not is_refresh_token(refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload["sub"]
    # Check token in DB
    result = await db.execute(select(Token).where(Token.token == refresh_token, Token.revoked == False))
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired or revoked")
    # Rotate refresh token
    new_refresh_token = create_refresh_token({"sub": user_id})
    db_token.revoked = True
    new_db_token = Token(
        user_id=uuid.UUID(user_id),
        token=new_refresh_token,
        type="refresh",
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_db_token)
    await db.commit()
    # Create new access token
    access_token = create_access_token({"sub": user_id})
    return access_token, new_refresh_token

async def revoke_token(token: str, db):
    result = await db.execute(select(Token).where(Token.token == token))
    db_token = result.scalar_one_or_none()
    if db_token:
        db_token.revoked = True
        await db.commit() 