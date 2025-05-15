from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .role import RoleResponse


# Request
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str
    roles: List[str]

# Response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    roles: List[RoleResponse]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password_hash: str