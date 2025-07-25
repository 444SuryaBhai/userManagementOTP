import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    mac = Column(String, nullable=True)
    login_at = Column(DateTime(timezone=True), server_default=func.now())
    logout_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions") 