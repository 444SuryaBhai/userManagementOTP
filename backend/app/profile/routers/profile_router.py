from fastapi import APIRouter, Depends, Request, status
from app.profile.schemas.profile_schema import ProfileResponse, ProfileUpdate
from app.profile.services.profile_service import get_profile, update_profile
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileResponse)
async def get_profile_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    user = await get_profile(user_id, db)
    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone,
        name=user.name,
        profile_pic=user.profile_pic,
        is_email_verified=user.is_email_verified,
        is_phone_verified=user.is_phone_verified,
        is_2fa_enabled=user.is_2fa_enabled
    )

@router.put("/", response_model=ProfileResponse)
async def update_profile_route(data: ProfileUpdate, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    user = await update_profile(user_id, data, db)
    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone,
        name=user.name,
        profile_pic=user.profile_pic,
        is_email_verified=user.is_email_verified,
        is_phone_verified=user.is_phone_verified,
        is_2fa_enabled=user.is_2fa_enabled
    ) 