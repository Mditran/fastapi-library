from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models.users import User as UserModel
from schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from  ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)