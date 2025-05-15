from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from models.users import User as UserModel
from schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from  ..database import get_db
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from schemas.loan import LoanCreate, LoanResponse, UserLoansResponse
from ..database import get_db
from ..oauth2 import require_roles
from schemas.token import TokenData
from models.loans import Loan as LoanModel
from models.books import Book as BookModel


router = APIRouter(
    prefix="/loans",
    tags=['Loans']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(require_roles(["ROLE_USER"]))):

    # 1. Buscar el libro
    book = db.query(BookModel).filter(BookModel.id == loan.book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {loan.book_id} was not found"
        )
    
    # 2. Verificar si ya tiene un préstamo activo para este libro
    existing_loan = db.query(LoanModel).filter(
        LoanModel.user_id == current_user.id,
        LoanModel.book_id == loan.book_id
    ).first()
    if existing_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already have an active loan for this book"
        )

    # 3. Verificar si hay copias disponibles
    if book.copies_available < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No copies available for book with id: {loan.book_id}"
        )

    # 4. Fechas
    loan_date = datetime.now(timezone.utc)
    return_date = loan_date + timedelta(days=90)

    # 5. Crear préstamo
    db_loan = LoanModel(
        user_id=current_user.id,
        loan_date=loan_date,
        return_date=return_date,
        **loan.model_dump()
    )
    db.add(db_loan)

    # 6. Actualizar copias
    book.copies_available -= 1

    # 7. Guardar
    db.commit()
    db.refresh(db_loan)

    return LoanResponse(
        book_id = db_loan.book_id,
        loan_id = db_loan.loan_id,
        user_name=db_loan.user.name,
        book_title=db_loan.book.title,
        loan_date=db_loan.loan_date,
        return_date=db_loan.return_date
    )

    
@router.get("/", response_model=UserLoansResponse)
def get_user_loans(db: Session = Depends(get_db), current_user: TokenData = Depends(require_roles(["ROLE_USER"]))):
    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
    loans = db.query(LoanModel).filter(LoanModel.user_id == current_user.id).all()
    if not loans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no registered loans"
        )

    return UserLoansResponse(
        user_name=user.name,
        loans=[
            LoanResponse(
                book_title=loan.book.title,
                loan_date=loan.loan_date,
                return_date=loan.return_date,
                book_id = loan.book_id,
                loan_id = loan.id,
            ) for loan in loans
        ])

@router.post("/{loan_id}/return", status_code=status.HTTP_200_OK)
def return_book(loan_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(require_roles(["ROLE_USER"]))):
    loan = db.query(LoanModel).filter(LoanModel.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    
    # 2. Verificar que el préstamo pertenece al usuario actual
    if loan.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to return this loan")
    
    book = db.query(BookModel).filter(BookModel.id == loan.book_id).first()
    if book:
        book.copies_available += 1
    db.delete(loan)
    db.commit()

    return {"message": "Book returned successfully"}