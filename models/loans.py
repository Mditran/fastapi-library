from sqlalchemy import Column, Integer, text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    loan_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    return_date = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")
