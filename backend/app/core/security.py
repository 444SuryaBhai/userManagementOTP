import pyotp
from passlib.context import CryptContext
from app.config.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2FA TOTP

def generate_2fa_secret():
    return pyotp.random_base32()

def get_totp_uri(secret: str, email: str):
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="UserManagement")

def verify_totp(token: str, secret: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

# Passwordless fallback (for future, if needed)
def hash_value(value: str) -> str:
    return pwd_context.hash(value)

def verify_hash(value: str, hashed: str) -> bool:
    return pwd_context.verify(value, hashed)

# User status helpers
def is_user_verified(user) -> bool:
    return user.is_email_verified and user.is_phone_verified

def is_2fa_enabled(user) -> bool:
    return user.is_2fa_enabled 