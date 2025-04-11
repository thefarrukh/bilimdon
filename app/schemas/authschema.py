from pydantic import BaseModel, EmailStr


class AuthRegistrationRequest(BaseModel):
    email: str
    password: str
    username: str

class AuthRegistrationResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active : bool
    is_staff : bool
    is_superuser : bool

    class Config:
        orm_mode = True


class AuthLogin(BaseModel):
    email: EmailStr
    password: str
