from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models.users import User as UserModel
from schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from  ..database import get_db
from typing import Optional, List
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)



def create_loan(user_id: int, book_id: int):
    loan_date = datetime.now(timezone.utc) 
    return_date = loan_date + timedelta(months=3)
    #loan = Loan(user_id=user_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
    
