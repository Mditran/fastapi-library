from pydantic import BaseModel, EmailStr

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True