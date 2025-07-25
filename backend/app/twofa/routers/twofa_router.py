from fastapi import APIRouter, Depends, Request, status
from app.twofa.schemas.twofa_schema import TwoFASetupResponse, TwoFAVerifyRequest, TwoFAStatusResponse
from app.twofa.services.twofa_service import setup_2fa, verify_2fa, disable_2fa
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/twofa", tags=["2FA"])

@router.post("/setup", response_model=TwoFASetupResponse)
async def setup_2fa_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    secret, qr_code_url = await setup_2fa(user_id, db)
    return TwoFASetupResponse(secret=secret, qr_code_url=qr_code_url)

@router.post("/verify", response_model=dict)
async def verify_2fa_route(data: TwoFAVerifyRequest, db: AsyncSession = Depends(get_db)):
    await verify_2fa(data.user_id, data.token, db)
    return {"message": "2FA verified and enabled"}

@router.post("/disable", response_model=dict)
async def disable_2fa_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    await disable_2fa(user_id, db)
    return {"message": "2FA disabled"}

@router.get("/status", response_model=TwoFAStatusResponse)
async def twofa_status_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    from app.models.user import User
    from sqlalchemy.future import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return TwoFAStatusResponse(is_2fa_enabled=user.is_2fa_enabled) 