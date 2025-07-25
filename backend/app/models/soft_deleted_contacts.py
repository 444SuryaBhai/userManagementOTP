import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class SoftDeletedContact(Base):
    __tablename__ = "soft_deleted_contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    contact_type = Column(String, nullable=False)  # email or phone
    value = Column(String, nullable=False)
    deleted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="soft_deleted_contacts") 