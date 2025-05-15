from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models.books import Book as BookModel
from schemas.book import BookCreate, BookResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..oauth2 import get_current_user, require_roles
from schemas.token import TokenData


router = APIRouter(
    prefix="/books",
    tags=['Books']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(require_roles(["ROLE_MODERATOR"]))):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books


@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id)
    if book.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    book.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookCreate, db: Session = Depends(get_db)):
    book_query = db.query(BookModel).filter(BookModel.id == id)
    if book_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    book_query.update(book.model_dump(), synchronize_session=False)
    db.commit()
    
    return  book_query.first()