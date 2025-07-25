from fastapi import APIRouter, Depends, Request, status
from app.settings.schemas.settings_schema import SettingsResponse, SettingsUpdate
from app.settings.services.settings_service import get_settings_service, update_settings_service
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/", response_model=SettingsResponse)
async def get_settings_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    is_2fa_enabled, account_status = await get_settings_service(user_id, db)
    return SettingsResponse(is_2fa_enabled=is_2fa_enabled, account_status=account_status)

@router.put("/", response_model=SettingsResponse)
async def update_settings_route(data: SettingsUpdate, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    user = await update_settings_service(user_id, data, db)
    return SettingsResponse(is_2fa_enabled=user.is_2fa_enabled, account_status=getattr(user, "account_status", "active")) 