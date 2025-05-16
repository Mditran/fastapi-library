from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..schemas.book import BookCreate, BookResponse
from ..models.books import Book as BookModel


def create_book_service(book: BookCreate, db: Session) -> BookResponse:
    # Validar si ya existe un libro con el mismo título y autor
    existing = db.query(BookModel).filter(
        BookModel.title == book.title,
        BookModel.author == book.author
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The book '{existing.title}' by '{existing.author}' is already registered with ID {existing.id}."
        )

    # Validar que las copias sean mayores a 0
    if book.copies_available < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The number of copies must be greater than 0."
        )

    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books_service(db: Session):
    books = db.query(BookModel).filter(BookModel.copies_available > 0).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no books available."
        )

    return books
