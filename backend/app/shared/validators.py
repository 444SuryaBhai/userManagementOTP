from email_validator import validate_email as ve, EmailNotValidError
import re

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")

def validate_email(email: str) -> bool:
    try:
        ve(email)
        return True
    except EmailNotValidError:
        return False

def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))

def validate_otp_format(otp: str) -> bool:
    return otp.isdigit() and len(otp) == 6 