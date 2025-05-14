from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

# Request
class UserCreate(UserBase):
    pass

# Response
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
