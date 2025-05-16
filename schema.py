from pydantic import BaseModel

class LoginRequest(BaseModel):
    mobile: str

class VerifyRequest(BaseModel):
    mobile: str
    user_otp: str
