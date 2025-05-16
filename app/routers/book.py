from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.book import BookCreate, BookResponse
from ..database import get_db
from ..oauth2 import require_roles
from ..schemas.token import TokenData
from ..services.book_service import create_book_service, get_books_service

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_roles(["ROLE_ADMIN", "ROLE_MODERATOR"]))
):
    return create_book_service(book, db)


@router.get("/", response_model=List[BookResponse])
def get_books(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_roles(["ROLE_ADMIN", "ROLE_MODERATOR", "ROLE_USER"]))
):
    return get_books_service(db)
