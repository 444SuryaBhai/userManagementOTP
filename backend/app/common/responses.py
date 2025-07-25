from pydantic import BaseModel

class SuccessResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str
    code: int

__all__ = ["SuccessResponse", "ErrorResponse"] 