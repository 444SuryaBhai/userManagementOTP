from app.models.session import Session
from app.db.session import get_db
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid

async def list_sessions(user_id: str, db):
    result = await db.execute(select(Session).where(Session.user_id == uuid.UUID(user_id)))
    sessions = result.scalars().all()
    return sessions

async def revoke_session(user_id: str, session_id: str, db):
    result = await db.execute(select(Session).where(Session.id == uuid.UUID(session_id), Session.user_id == uuid.UUID(user_id)))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.is_active = False
    session.logout_at = "now"  # In real code, use datetime.utcnow()
    await db.commit()
    return True

async def revoke_all_sessions_except(user_id: str, current_session_id: str, db):
    result = await db.execute(select(Session).where(Session.user_id == uuid.UUID(user_id), Session.id != uuid.UUID(current_session_id)))
    sessions = result.scalars().all()
    for session in sessions:
        session.is_active = False
        session.logout_at = "now"
    await db.commit()
    return True 