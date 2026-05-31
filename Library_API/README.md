# Simple Library Manager

## 1. Project Overview

Simple Library Manager is a small library management system built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Gradio**.

This project allows users to manage books, readers, and book loans through both a REST API and a visual web interface.

The main goal of this project is to practice backend development, database modeling, CRUD operations, and simple user interface design.

---

## 2. Main Features

### Book Management

- Add new books
- View all books
- Update book information
- Delete books
- Check whether a book is available or loaned

### Reader Management

- Add new readers
- View all readers
- Update reader information
- Delete readers

### Loan Management

- Create a book loan
- Return a book
- View all loan records
- View active loans
- View overdue loans

### Dashboard

- Total books
- Available books
- Loaned books
- Total readers
- Total loan records
- Overdue loan count

---

## 3. Technologies Used

| Part | Technology |
|---|---|
| Backend API | FastAPI |
| Database ORM | SQLAlchemy |
| Database | SQLite |
| Data Validation | Pydantic |
| UI | Gradio |
| Language | Python |

---

## 4. Project Structure

```text
Library_API/
├── database.py
├── models.py
├── crud.py
├── main.py
├── gradio_app.py
├── requirements.txt
└── README.md
```

---

## 5. File Description

| File | Description |
|---|---|
| `database.py` | Manages database connection and session creation |
| `models.py` | Defines SQLAlchemy models and Pydantic schemas |
| `crud.py` | Contains business logic and database operations |
| `main.py` | Defines FastAPI application and API endpoints |
| `gradio_app.py` | Provides a visual web interface using Gradio |
| `requirements.txt` | Lists required Python packages |

---

## 6. Database Tables

### books

| Column | Description |
|---|---|
| `id` | Book ID |
| `title` | Book title |
| `author` | Book author |
| `is_available` | Book availability status |

### readers

| Column | Description |
|---|---|
| `id` | Reader ID |
| `name` | Reader name |
| `phone` | Reader phone number |

### loans

| Column | Description |
|---|---|
| `id` | Loan ID |
| `book_id` | Book foreign key |
| `reader_id` | Reader foreign key |
| `loan_date` | Loan start date |
| `due_date` | Expected return date |
| `return_date` | Actual return date |

---

## 7. API Endpoints

### Books

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/books/` | Create a new book |
| `GET` | `/books/` | Get all books |
| `GET` | `/books/{book_id}` | Get one book |
| `PUT` | `/books/{book_id}` | Update book information |
| `DELETE` | `/books/{book_id}` | Delete a book |

### Readers

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/readers/` | Create a new reader |
| `GET` | `/readers/` | Get all readers |
| `GET` | `/readers/{reader_id}` | Get one reader |
| `PUT` | `/readers/{reader_id}` | Update reader information |
| `DELETE` | `/readers/{reader_id}` | Delete a reader |

### Loans

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/loans/` | Create a new loan |
| `GET` | `/loans/` | Get all loans |
| `GET` | `/loans/active` | Get active loans |
| `GET` | `/loans/overdue` | Get overdue loans |
| `GET` | `/loans/{loan_id}` | Get one loan |
| `PATCH` | `/loans/{loan_id}/return` | Return a book |

---

# 간단한 도서관 관리 시스템

## 1. 프로젝트 개요

Simple Library Manager는 **FastAPI**, **SQLAlchemy**, **SQLite**, **Gradio**를 사용하여 만든 간단한 도서관 관리 시스템입니다.

이 프로젝트는 REST API와 시각적인 웹 인터페이스를 통해 도서, 독자, 도서 대출 정보를 관리할 수 있습니다.

이 프로젝트의 주요 목적은 백엔드 개발, 데이터베이스 모델링, CRUD 기능 구현, 간단한 사용자 인터페이스 설계를 연습하는 것입니다.

---

## 2. 주요 기능

### 도서 관리

- 새 도서 등록
- 전체 도서 조회
- 도서 정보 수정
- 도서 삭제
- 도서가 대출 가능한지 또는 대출 중인지 확인

### 독자 관리

- 새 독자 등록
- 전체 독자 조회
- 독자 정보 수정
- 독자 삭제

### 대출 관리

- 도서 대출 등록
- 도서 반납 처리
- 전체 대출 기록 조회
- 현재 대출 중인 목록 조회
- 연체 목록 조회

### 대시보드

- 전체 도서 수
- 대출 가능한 도서 수
- 대출 중인 도서 수
- 전체 독자 수
- 전체 대출 기록 수
- 연체 대출 수

---

## 3. 사용 기술

| 구분 | 기술 |
|---|---|
| Backend API | FastAPI |
| Database ORM | SQLAlchemy |
| Database | SQLite |
| Data Validation | Pydantic |
| UI | Gradio |
| Language | Python |

---

## 4. 프로젝트 구조

```text
Library_API/
├── database.py
├── models.py
├── crud.py
├── main.py
├── gradio_app.py
├── requirements.txt
└── README.md
```

---

## 5. 파일 설명

| 파일 | 설명 |
|---|---|
| `database.py` | 데이터베이스 연결 및 세션 생성을 관리합니다 |
| `models.py` | SQLAlchemy 모델과 Pydantic 스키마를 정의합니다 |
| `crud.py` | 비즈니스 로직과 데이터베이스 작업을 포함합니다 |
| `main.py` | FastAPI 애플리케이션과 API 엔드포인트를 정의합니다 |
| `gradio_app.py` | Gradio를 사용한 시각적 웹 인터페이스를 제공합니다 |
| `requirements.txt` | 필요한 Python 패키지 목록을 포함합니다 |

---

## 6. 데이터베이스 테이블

### books

| 컬럼 | 설명 |
|---|---|
| `id` | 도서 ID |
| `title` | 도서 제목 |
| `author` | 저자 |
| `is_available` | 도서 대출 가능 상태 |

### readers

| 컬럼 | 설명 |
|---|---|
| `id` | 독자 ID |
| `name` | 독자 이름 |
| `phone` | 독자 전화번호 |

### loans

| 컬럼 | 설명 |
|---|---|
| `id` | 대출 ID |
| `book_id` | 도서 외래키 |
| `reader_id` | 독자 외래키 |
| `loan_date` | 대출 시작일 |
| `due_date` | 반납 예정일 |
| `return_date` | 실제 반납일 |

---

## 7. API 엔드포인트

### Books

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/books/` | 새 도서 등록 |
| `GET` | `/books/` | 전체 도서 조회 |
| `GET` | `/books/{book_id}` | 특정 도서 조회 |
| `PUT` | `/books/{book_id}` | 도서 정보 수정 |
| `DELETE` | `/books/{book_id}` | 도서 삭제 |

### Readers

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/readers/` | 새 독자 등록 |
| `GET` | `/readers/` | 전체 독자 조회 |
| `GET` | `/readers/{reader_id}` | 특정 독자 조회 |
| `PUT` | `/readers/{reader_id}` | 독자 정보 수정 |
| `DELETE` | `/readers/{reader_id}` | 독자 삭제 |

### Loans

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/loans/` | 새 대출 등록 |
| `GET` | `/loans/` | 전체 대출 조회 |
| `GET` | `/loans/active` | 현재 대출 중인 목록 조회 |
| `GET` | `/loans/overdue` | 연체 목록 조회 |
| `GET` | `/loans/{loan_id}` | 특정 대출 조회 |
| `PATCH` | `/loans/{loan_id}/return` | 도서 반납 처리 |
