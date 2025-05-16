from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

from ..models.books import Book as BookModel
from ..models.loans import Loan as LoanModel
from ..models.users import User as UserModel
from ..schemas.loan import LoanCreate, LoanResponse, UserLoansResponse
from ..schemas.token import TokenData


def create_loan_service(db: Session, loan: LoanCreate, current_user: TokenData) -> LoanResponse:
    book = db.query(BookModel).filter(BookModel.id == loan.book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id: {loan.book_id} was not found")

    existing_loan = db.query(LoanModel).filter(
        LoanModel.user_id == current_user.id,
        LoanModel.book_id == loan.book_id,
        LoanModel.return_date > datetime.now(timezone.utc)
    ).first()
    if existing_loan:
        raise HTTPException(status_code=400, detail="You already have an active loan for this book")

    if book.copies_available < 1:
        raise HTTPException(status_code=400, detail="No copies available for this book")

    loan_date = datetime.now(timezone.utc)
    return_date = loan_date + timedelta(days=90)

    db_loan = LoanModel(
        user_id=current_user.id,
        loan_date=loan_date,
        return_date=return_date,
        **loan.model_dump()
    )
    db.add(db_loan)
    book.copies_available -= 1
    db.commit()
    db.refresh(db_loan)

    return LoanResponse(
        book_id=db_loan.book_id,
        loan_id=db_loan.loan_id,
        user_name=db_loan.user.name,
        book_title=db_loan.book.title,
        loan_date=db_loan.loan_date,
        return_date=db_loan.return_date
    )


def get_user_loans_service(db: Session, current_user: TokenData) -> UserLoansResponse:
    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
    loans = db.query(LoanModel).filter(
        LoanModel.user_id == current_user.id,
        LoanModel.return_date > datetime.now(timezone.utc)
    ).all()

    if not loans:
        raise HTTPException(status_code=404, detail="User has no active loans")

    return UserLoansResponse(
        user_name=user.name,
        loans=[
            LoanResponse(
                book_title=loan.book.title,
                loan_date=loan.loan_date,
                return_date=loan.return_date,
                book_id=loan.book_id,
                loan_id=loan.id,
            ) for loan in loans
        ]
    )


def return_book_service(db: Session, loan_id: int, current_user: TokenData):
    loan = db.query(LoanModel).filter(LoanModel.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to return this loan")

    if loan.return_date <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="This book has already been returned")

    loan.return_date = datetime.now(timezone.utc)

    book = db.query(BookModel).filter(BookModel.id == loan.book_id).first()
    if book:
        book.copies_available += 1

    db.commit()
    return {"message": "Book returned successfully"}
