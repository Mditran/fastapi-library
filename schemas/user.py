from pydantic import BaseModel, EmailStr
from typing import Optional


# Request
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str

# Response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
