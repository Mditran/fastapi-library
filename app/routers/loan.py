from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..schemas.loan import LoanCreate, LoanResponse, UserLoansResponse
from ..database import get_db
from ..schemas.token import TokenData
from ..oauth2 import require_roles
from ..services.loan_service import (
    create_loan_service,
    get_user_loans_service,
    return_book_service
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LoanResponse)
def create_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_roles(["ROLE_USER"]))
):
    return create_loan_service(db, loan, current_user)

@router.get("/", response_model=UserLoansResponse)
def get_user_loans(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_roles(["ROLE_USER"]))
):
    return get_user_loans_service(db, current_user)

@router.post("/{loan_id}/return", status_code=status.HTTP_200_OK)
def return_book(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_roles(["ROLE_USER"]))
):
    return return_book_service(db, loan_id, current_user)
