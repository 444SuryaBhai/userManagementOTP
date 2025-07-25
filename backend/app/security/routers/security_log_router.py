from fastapi import APIRouter, Depends, Request, status
from app.security.schemas.security_log_schema import SecurityLogListResponse, SecurityLogResponse
from app.security.services.security_log_service import list_security_logs
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/security/logs", tags=["Security Logs"])

@router.get("/", response_model=SecurityLogListResponse)
async def list_security_logs_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    logs = await list_security_logs(user_id, db)
    return SecurityLogListResponse(logs=[SecurityLogResponse(
        id=str(l.id),
        action=l.action,
        ip=l.ip,
        device=l.device,
        created_at=str(l.created_at)
    ) for l in logs]) 