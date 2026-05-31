from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from models import (
    DBBook,
    DBReader,
    DBLoan,
    BookCreate,
    BookUpdate,
    ReaderCreate,
    ReaderUpdate,
    LoanCreate,
    LoanReturn
)


# =========================
# BOOK CRUD
# =========================

def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        author=book.author,
        is_available=True
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books(db: Session) -> List[DBBook]:
    return db.query(DBBook).all()


def get_book(db: Session, book_id: int) -> Optional[DBBook]:
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def update_book(db: Session, book_id: int, book_data: BookUpdate) -> Optional[DBBook]:
    db_book = get_book(db, book_id)

    if db_book is None:
        return None

    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)

    if db_book is None:
        return False

    active_loan = (
        db.query(DBLoan)
        .filter(DBLoan.book_id == book_id)
        .filter(DBLoan.return_date == None)
        .first()
    )

    if active_loan is not None:
        return False

    db.delete(db_book)
    db.commit()

    return True


# =========================
# READER CRUD
# =========================

def create_reader(db: Session, reader: ReaderCreate) -> DBReader:
    db_reader = DBReader(
        name=reader.name,
        phone=reader.phone
    )

    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)

    return db_reader


def get_readers(db: Session) -> List[DBReader]:
    return db.query(DBReader).all()


def get_reader(db: Session, reader_id: int) -> Optional[DBReader]:
    return db.query(DBReader).filter(DBReader.id == reader_id).first()


def update_reader(db: Session, reader_id: int, reader_data: ReaderUpdate) -> Optional[DBReader]:
    db_reader = get_reader(db, reader_id)

    if db_reader is None:
        return None

    update_data = reader_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_reader, field, value)

    db.commit()
    db.refresh(db_reader)

    return db_reader


def delete_reader(db: Session, reader_id: int) -> bool:
    db_reader = get_reader(db, reader_id)

    if db_reader is None:
        return False

    active_loan = (
        db.query(DBLoan)
        .filter(DBLoan.reader_id == reader_id)
        .filter(DBLoan.return_date == None)
        .first()
    )

    if active_loan is not None:
        return False

    db.delete(db_reader)
    db.commit()

    return True


# =========================
# LOAN CRUD
# =========================

def create_loan(db: Session, loan: LoanCreate):
    db_book = get_book(db, loan.book_id)

    if db_book is None:
        return None, "Book not found"

    if db_book.is_available is False:
        return None, "Book is already loaned"

    db_reader = get_reader(db, loan.reader_id)

    if db_reader is None:
        return None, "Reader not found"

    db_loan = DBLoan(
        book_id=loan.book_id,
        reader_id=loan.reader_id,
        loan_date=loan.loan_date,
        due_date=loan.due_date,
        return_date=None
    )

    db_book.is_available = False

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return db_loan, None


def get_loans(db: Session) -> List[DBLoan]:
    return db.query(DBLoan).all()


def get_loan(db: Session, loan_id: int) -> Optional[DBLoan]:
    return db.query(DBLoan).filter(DBLoan.id == loan_id).first()


def get_active_loans(db: Session) -> List[DBLoan]:
    return db.query(DBLoan).filter(DBLoan.return_date == None).all()


def get_overdue_loans(db: Session) -> List[DBLoan]:
    today = date.today()

    return (
        db.query(DBLoan)
        .filter(DBLoan.return_date == None)
        .filter(DBLoan.due_date < today)
        .all()
    )


def return_book(db: Session, loan_id: int, return_data: LoanReturn):
    db_loan = get_loan(db, loan_id)

    if db_loan is None:
        return None, "Loan not found"

    if db_loan.return_date is not None:
        return None, "Book already returned"

    db_book = get_book(db, db_loan.book_id)

    if db_book is None:
        return None, "Book not found"

    db_loan.return_date = return_data.return_date
    db_book.is_available = True

    db.commit()
    db.refresh(db_loan)

    return db_loan, None