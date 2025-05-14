from sqlalchemy import Column, Integer, Enum
from ERole import ERole
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Enum(ERole), nullable=False)
