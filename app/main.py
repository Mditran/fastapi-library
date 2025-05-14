from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from models.users import User as UserModel
from models.books import Book as BookModel
from schemas.book import BookCreate, BookResponse
from typing import Optional, List

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the best online library!!"}

@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books


@app.get("/books/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    return book


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id)
    if book.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    book.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/books/{id}", response_model=BookResponse)
def update_book(id: int, book: BookCreate, db: Session = Depends(get_db)):
    book_query = db.query(BookModel).filter(BookModel.id == id)
    if book_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    book_query.update(book.model_dump(), synchronize_session=False)
    db.commit()
    
    return  book_query.first()