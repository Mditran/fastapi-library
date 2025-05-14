from sqlalchemy import Column, Integer, text, DateTime
from app.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    book_id = Column(Integer, unique=True, nullable=False)
    loan_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    return_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP + interval '3 months'"))
