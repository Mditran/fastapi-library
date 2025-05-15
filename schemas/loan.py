from pydantic import BaseModel
from datetime import datetime
from typing import List

# Request
class LoanCreate(BaseModel):
    book_id: int

# Response
class LoanResponse(LoanCreate):
    book_title: str
    loan_date: datetime
    return_date: datetime
    loan_id: int

    class Config:
        from_attributes = True

class UserLoansResponse(BaseModel):
    user_name: str
    loans: List[LoanResponse]
