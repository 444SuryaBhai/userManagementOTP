from app.models.trusted_device import TrustedDevice
from app.db.session import get_db
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid
from datetime import datetime

async def list_trusted_devices(user_id: str, db):
    result = await db.execute(select(TrustedDevice).where(TrustedDevice.user_id == uuid.UUID(user_id)))
    devices = result.scalars().all()
    return devices

async def add_trusted_device(user_id: str, data, db):
    device = TrustedDevice(
        user_id=uuid.UUID(user_id),
        device_info=data.device_info,
        ip=data.ip,
        mac=data.mac,
        added_at=datetime.utcnow(),
        is_active=True
    )
    db.add(device)
    await db.commit()
    return device

async def remove_trusted_device(user_id: str, device_id: str, db):
    result = await db.execute(select(TrustedDevice).where(TrustedDevice.id == uuid.UUID(device_id), TrustedDevice.user_id == uuid.UUID(user_id)))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Trusted device not found")
    device.is_active = False
    await db.commit()
    return True 