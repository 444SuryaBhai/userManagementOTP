from fastapi import APIRouter, Depends, Request, status
from app.sessions.schemas.session_schema import SessionListResponse, SessionRevokeRequest, SessionResponse
from app.sessions.services.session_service import list_sessions, revoke_session, revoke_all_sessions_except
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("/", response_model=SessionListResponse)
async def list_sessions_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    sessions = await list_sessions(user_id, db)
    return SessionListResponse(sessions=[SessionResponse(
        id=str(s.id),
        device=s.device,
        ip=s.ip,
        mac=s.mac,
        login_at=str(s.login_at) if s.login_at else None,
        logout_at=str(s.logout_at) if s.logout_at else None,
        is_active=s.is_active
    ) for s in sessions])

@router.post("/revoke", response_model=dict)
async def revoke_session_route(data: SessionRevokeRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    await revoke_session(user_id, data.session_id, db)
    return {"message": "Session revoked"}

@router.post("/revoke-all", response_model=dict)
async def revoke_all_sessions_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    current_session_id = request.cookies.get("session")
    await revoke_all_sessions_except(user_id, current_session_id, db)
    return {"message": "All other sessions revoked"} 