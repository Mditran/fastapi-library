from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .user_roles import User_Roles


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    roles = relationship("Role", secondary=User_Roles, back_populates="users")
    loans = relationship("Loan", back_populates="user")
