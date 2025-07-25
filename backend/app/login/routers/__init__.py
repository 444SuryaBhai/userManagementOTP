from .email_otp_router import router as email_otp_router
from .phone_otp_router import router as phone_otp_router
from .oauth_router import router as oauth_router

__all__ = ["email_otp_router", "phone_otp_router", "oauth_router"] 