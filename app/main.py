from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from models.users import User as UserModel
from models.books import Book as BookModel

app = FastAPI()

Base.metadata.create_all(bind=engine)
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Book(BaseModel):
    title: str
    author: str
    copies_available: int

my_books = [
    {
        "id": 1,
        "title": 'Cronicas de una muerte anunciada',
        "author": 'Gabriel Garcia',
        "copies_available": 1
    },
    {
        "id": 2,
        "title": 'El complot',
        "author": 'Irving Wallace',
        "copies_available": 5
    },
]

def find_book(id):
    for book in my_books:
        if book['id'] == id:
            return book
        
def find_index(id):
    for i, book in enumerate(my_books):
        if book['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to the best online library!!"}

@app.get("/books")
def get_posts():
    return {"data": my_books}

@app.get("/books/{id}")
def get_posts(id: int, response: Response):
    book = find_book(int(id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f"Book not found"} """
    return {"data": book}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_posts(book: Book):
    print(book)
    book_dict = book.model_dump()
    book_dict['id'] = randrange(0, 10000)
    my_books.append(book_dict)
    return {"data": book_dict}

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    my_books.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/books/{id}", status_code=status.HTTP_201_CREATED)
def create_posts(id: int, book: Book):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {id} was not found")
    book_dict = book.model_dump()
    book_dict['id'] = id
    my_books[index] = book_dict
    return {"messege": f"Updated book"}

@app.post("/sqlalchemy")
def test_books(book: Book, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book