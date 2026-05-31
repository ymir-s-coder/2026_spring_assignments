from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
from datetime import date

from database import Base


# =========================
# SQLALCHEMY MODELS
# =========================

class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)

    loans = relationship("DBLoan", back_populates="book")


class DBReader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)

    loans = relationship("DBLoan", back_populates="reader")


class DBLoan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)

    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    book = relationship("DBBook", back_populates="loans")
    reader = relationship("DBReader", back_populates="loans")


# =========================
# PYDANTIC SCHEMAS
# =========================

class BookCreate(BaseModel):
    title: str
    author: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    is_available: Optional[bool] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool

    class Config:
        from_attributes = True


class ReaderCreate(BaseModel):
    name: str
    phone: Optional[str] = None


class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class ReaderResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str]

    class Config:
        from_attributes = True


class LoanCreate(BaseModel):
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date


class LoanReturn(BaseModel):
    return_date: date


class LoanResponse(BaseModel):
    id: int
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date]

    book: BookResponse
    reader: ReaderResponse

    class Config:
        from_attributes = True