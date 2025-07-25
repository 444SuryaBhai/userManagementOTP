from fastapi import HTTPException, status

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

class InvalidOTPException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

class RateLimitException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

__all__ = ["UserNotFoundException", "InvalidOTPException", "RateLimitException"] 