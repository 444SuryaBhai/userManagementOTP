import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    is_2fa_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    otps = relationship("OTP", back_populates="user", cascade="all, delete-orphan")
    trusted_devices = relationship("TrustedDevice", back_populates="user", cascade="all, delete-orphan")
    security_logs = relationship("SecurityLog", back_populates="user", cascade="all, delete-orphan")
    soft_deleted_contacts = relationship("SoftDeletedContact", back_populates="user", cascade="all, delete-orphan") 