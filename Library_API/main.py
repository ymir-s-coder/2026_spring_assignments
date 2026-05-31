from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
import crud

from models import (
    BookCreate,
    BookUpdate,
    BookResponse,
    ReaderCreate,
    ReaderUpdate,
    ReaderResponse,
    LoanCreate,
    LoanReturn,
    LoanResponse
)


app = FastAPI(
    title="Simple Library API",
    description="Simple library management system with books, readers and loans",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Simple Library API is running",
        "docs": "http://127.0.0.1:8000/docs",
        "gradio": "Run python gradio_app.py"
    }


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# =========================
# BOOKS
# =========================

@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
):
    book = crud.update_book(db, book_id, book_data)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    result = crud.delete_book(db, book_id)

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Book not found or book has active loan"
        )

    return {
        "message": f"Book with id={book_id} deleted successfully"
    }


# =========================
# READERS
# =========================

@app.post("/readers/", response_model=ReaderResponse)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db, reader)


@app.get("/readers/", response_model=List[ReaderResponse])
def get_readers(db: Session = Depends(get_db)):
    return crud.get_readers(db)


@app.get("/readers/{reader_id}", response_model=ReaderResponse)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = crud.get_reader(db, reader_id)

    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")

    return reader


@app.put("/readers/{reader_id}", response_model=ReaderResponse)
def update_reader(
    reader_id: int,
    reader_data: ReaderUpdate,
    db: Session = Depends(get_db)
):
    reader = crud.update_reader(db, reader_id, reader_data)

    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")

    return reader


@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    result = crud.delete_reader(db, reader_id)

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Reader not found or reader has active loan"
        )

    return {
        "message": f"Reader with id={reader_id} deleted successfully"
    }


# =========================
# LOANS
# =========================

@app.post("/loans/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    result, error = crud.create_loan(db, loan)

    if result is None:
        raise HTTPException(status_code=400, detail=error)

    return result


@app.get("/loans/", response_model=List[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    return crud.get_loans(db)


@app.get("/loans/active", response_model=List[LoanResponse])
def get_active_loans(db: Session = Depends(get_db)):
    return crud.get_active_loans(db)


@app.get("/loans/overdue", response_model=List[LoanResponse])
def get_overdue_loans(db: Session = Depends(get_db)):
    return crud.get_overdue_loans(db)


@app.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.get_loan(db, loan_id)

    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan


@app.patch("/loans/{loan_id}/return", response_model=LoanResponse)
def return_book(
    loan_id: int,
    return_data: LoanReturn,
    db: Session = Depends(get_db)
):
    result, error = crud.return_book(db, loan_id, return_data)

    if result is None:
        raise HTTPException(status_code=400, detail=error)

    return result