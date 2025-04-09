from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthRegistration(BaseModel):
    username: str
    password: str
    email: str

class AuthRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True


class AuthLogin(BaseModel):
    username: str
    password: str