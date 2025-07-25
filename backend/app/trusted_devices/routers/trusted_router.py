from fastapi import APIRouter, Depends, Request, status
from app.trusted_devices.schemas.trusted_schema import TrustedDeviceListResponse, TrustedDeviceResponse, TrustedDeviceAddRequest
from app.trusted_devices.services.trusted_service import list_trusted_devices, add_trusted_device, remove_trusted_device
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/trusted-devices", tags=["Trusted Devices"])

@router.get("/", response_model=TrustedDeviceListResponse)
async def list_trusted_devices_route(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    devices = await list_trusted_devices(user_id, db)
    return TrustedDeviceListResponse(devices=[TrustedDeviceResponse(
        id=str(d.id),
        device_info=d.device_info,
        ip=d.ip,
        mac=d.mac,
        added_at=str(d.added_at) if d.added_at else None,
        is_active=d.is_active
    ) for d in devices])

@router.post("/add", response_model=TrustedDeviceResponse)
async def add_trusted_device_route(data: TrustedDeviceAddRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    device = await add_trusted_device(user_id, data, db)
    return TrustedDeviceResponse(
        id=str(device.id),
        device_info=device.device_info,
        ip=device.ip,
        mac=device.mac,
        added_at=str(device.added_at) if device.added_at else None,
        is_active=device.is_active
    )

@router.post("/remove", response_model=dict)
async def remove_trusted_device_route(device_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user["sub"]
    await remove_trusted_device(user_id, device_id, db)
    return {"message": "Trusted device removed"} 