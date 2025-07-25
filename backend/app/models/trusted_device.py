import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class TrustedDevice(Base):
    __tablename__ = "trusted_devices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_info = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    mac = Column(String, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="trusted_devices") 