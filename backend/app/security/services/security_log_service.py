from app.models.security_log import SecurityLog
from app.db.session import get_db
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid
from datetime import datetime

async def list_security_logs(user_id: str, db):
    result = await db.execute(select(SecurityLog).where(SecurityLog.user_id == uuid.UUID(user_id)))
    logs = result.scalars().all()
    return logs

async def add_security_log(user_id: str, action: str, ip: str = None, device: str = None, db=None):
    log = SecurityLog(
        user_id=uuid.UUID(user_id),
        action=action,
        ip=ip,
        device=device,
        created_at=datetime.utcnow()
    )
    db.add(log)
    await db.commit()
    return log 