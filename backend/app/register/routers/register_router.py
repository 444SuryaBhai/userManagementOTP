from fastapi import APIRouter, Depends, status
from app.register.schemas.register_schema import RegisterInput, RegisterResponse
from app.register.services.register_service import register_user
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/register", tags=["Register"])

@router.post("/", response_model=RegisterResponse)
async def register(data: RegisterInput, db: AsyncSession = Depends(get_db)):
    user_id, autofill = await register_user(data, db)
    return RegisterResponse(user_id=user_id, message="Registration successful. OTPs sent to email and phone.") 