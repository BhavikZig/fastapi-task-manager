from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True