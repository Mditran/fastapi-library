from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models.users import User as UserModel
from schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from  ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_book(user: UserCreate, db: Session = Depends(get_db)):

    user.password_hash = hash(user.password_hash)

    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user