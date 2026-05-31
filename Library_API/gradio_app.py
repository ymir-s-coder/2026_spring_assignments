import gradio as gr
import pandas as pd

from datetime import date

from database import Base, engine, SessionLocal
import crud

from models import (
    BookCreate,
    BookUpdate,
    ReaderCreate,
    ReaderUpdate,
    LoanCreate,
    LoanReturn
)


# =========================
# DATABASE INIT
# =========================

Base.metadata.create_all(bind=engine)


def get_db_session():
    return SessionLocal()


# =========================
# HELPERS
# =========================

def safe_int(value):
    if value is None:
        return None
    return int(value)


def format_bool(value):
    return "Available" if value else "Loaned"


def get_dashboard_data():
    db = get_db_session()

    try:
        books = crud.get_books(db)
        readers = crud.get_readers(db)
        loans = crud.get_loans(db)
        active_loans = crud.get_active_loans(db)
        overdue_loans = crud.get_overdue_loans(db)

        total_books = len(books)
        available_books = len([book for book in books if book.is_available])
        loaned_books = total_books - available_books

        total_readers = len(readers)
        total_loans = len(loans)
        active_count = len(active_loans)
        overdue_count = len(overdue_loans)

        summary = f"""
        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-label">Total Books</div>
                <div class="stat-value">{total_books}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Available Books</div>
                <div class="stat-value">{available_books}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Loaned Books</div>
                <div class="stat-value">{loaned_books}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Readers</div>
                <div class="stat-value">{total_readers}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Loans</div>
                <div class="stat-value">{total_loans}</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-label">Overdue Loans</div>
                <div class="stat-value">{overdue_count}</div>
            </div>
        </div>
        """

        return summary

    finally:
        db.close()


def books_to_dataframe(books):
    rows = []

    for book in books:
        rows.append({
            "ID": book.id,
            "Title": book.title,
            "Author": book.author,
            "Status": format_bool(book.is_available)
        })

    return pd.DataFrame(rows)


def readers_to_dataframe(readers):
    rows = []

    for reader in readers:
        rows.append({
            "ID": reader.id,
            "Name": reader.name,
            "Phone": reader.phone
        })

    return pd.DataFrame(rows)


def loans_to_dataframe(loans):
    rows = []

    for loan in loans:
        status = "Returned" if loan.return_date else "Active"

        rows.append({
            "ID": loan.id,
            "Book": loan.book.title,
            "Reader": loan.reader.name,
            "Loan Date": loan.loan_date,
            "Due Date": loan.due_date,
            "Return Date": loan.return_date,
            "Status": status
        })

    return pd.DataFrame(rows)


# =========================
# BOOK FUNCTIONS
# =========================

def ui_get_books():
    db = get_db_session()

    try:
        books = crud.get_books(db)
        return books_to_dataframe(books)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

    finally:
        db.close()


def ui_create_book(title, author):
    db = get_db_session()

    try:
        if not title or not author:
            return "Please enter book title and author.", ui_get_books(), get_dashboard_data()

        book = crud.create_book(
            db,
            BookCreate(
                title=title.strip(),
                author=author.strip()
            )
        )

        message = f"Book created successfully. ID={book.id}"

        return message, ui_get_books(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_books(), get_dashboard_data()

    finally:
        db.close()


def ui_update_book(book_id, title, author, is_available):
    db = get_db_session()

    try:
        if book_id is None:
            return "Please enter book ID.", ui_get_books(), get_dashboard_data()

        book_data = BookUpdate(
            title=title.strip() if title else None,
            author=author.strip() if author else None,
            is_available=is_available
        )

        book = crud.update_book(db, safe_int(book_id), book_data)

        if book is None:
            return "Book not found.", ui_get_books(), get_dashboard_data()

        message = f"Book updated successfully. ID={book.id}"

        return message, ui_get_books(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_books(), get_dashboard_data()

    finally:
        db.close()


def ui_delete_book(book_id):
    db = get_db_session()

    try:
        if book_id is None:
            return "Please enter book ID.", ui_get_books(), get_dashboard_data()

        result = crud.delete_book(db, safe_int(book_id))

        if result is False:
            return "Cannot delete book. Book not found or has active loan.", ui_get_books(), get_dashboard_data()

        message = f"Book deleted successfully. ID={safe_int(book_id)}"

        return message, ui_get_books(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_books(), get_dashboard_data()

    finally:
        db.close()


# =========================
# READER FUNCTIONS
# =========================

def ui_get_readers():
    db = get_db_session()

    try:
        readers = crud.get_readers(db)
        return readers_to_dataframe(readers)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

    finally:
        db.close()


def ui_create_reader(name, phone):
    db = get_db_session()

    try:
        if not name:
            return "Please enter reader name.", ui_get_readers(), get_dashboard_data()

        reader = crud.create_reader(
            db,
            ReaderCreate(
                name=name.strip(),
                phone=phone.strip() if phone else None
            )
        )

        message = f"Reader created successfully. ID={reader.id}"

        return message, ui_get_readers(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_readers(), get_dashboard_data()

    finally:
        db.close()


def ui_update_reader(reader_id, name, phone):
    db = get_db_session()

    try:
        if reader_id is None:
            return "Please enter reader ID.", ui_get_readers(), get_dashboard_data()

        reader_data = ReaderUpdate(
            name=name.strip() if name else None,
            phone=phone.strip() if phone else None
        )

        reader = crud.update_reader(db, safe_int(reader_id), reader_data)

        if reader is None:
            return "Reader not found.", ui_get_readers(), get_dashboard_data()

        message = f"Reader updated successfully. ID={reader.id}"

        return message, ui_get_readers(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_readers(), get_dashboard_data()

    finally:
        db.close()


def ui_delete_reader(reader_id):
    db = get_db_session()

    try:
        if reader_id is None:
            return "Please enter reader ID.", ui_get_readers(), get_dashboard_data()

        result = crud.delete_reader(db, safe_int(reader_id))

        if result is False:
            return "Cannot delete reader. Reader not found or has active loan.", ui_get_readers(), get_dashboard_data()

        message = f"Reader deleted successfully. ID={safe_int(reader_id)}"

        return message, ui_get_readers(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_readers(), get_dashboard_data()

    finally:
        db.close()


# =========================
# LOAN FUNCTIONS
# =========================

def ui_get_loans():
    db = get_db_session()

    try:
        loans = crud.get_loans(db)
        return loans_to_dataframe(loans)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

    finally:
        db.close()


def ui_get_active_loans():
    db = get_db_session()

    try:
        loans = crud.get_active_loans(db)
        return loans_to_dataframe(loans)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

    finally:
        db.close()


def ui_get_overdue_loans():
    db = get_db_session()

    try:
        loans = crud.get_overdue_loans(db)
        return loans_to_dataframe(loans)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

    finally:
        db.close()


def ui_create_loan(book_id, reader_id, loan_date, due_date):
    db = get_db_session()

    try:
        if book_id is None or reader_id is None:
            return "Please enter book ID and reader ID.", ui_get_loans(), get_dashboard_data()

        if not loan_date or not due_date:
            return "Please enter loan date and due date.", ui_get_loans(), get_dashboard_data()

        loan, error = crud.create_loan(
            db,
            LoanCreate(
                book_id=safe_int(book_id),
                reader_id=safe_int(reader_id),
                loan_date=date.fromisoformat(loan_date),
                due_date=date.fromisoformat(due_date)
            )
        )

        if loan is None:
            return error, ui_get_loans(), get_dashboard_data()

        message = f"Loan created successfully. ID={loan.id}"

        return message, ui_get_loans(), get_dashboard_data()

    except ValueError:
        return "Date format must be YYYY-MM-DD. Example: 2026-06-01", ui_get_loans(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_loans(), get_dashboard_data()

    finally:
        db.close()


def ui_return_book(loan_id, return_date):
    db = get_db_session()

    try:
        if loan_id is None:
            return "Please enter loan ID.", ui_get_loans(), get_dashboard_data()

        if not return_date:
            return "Please enter return date.", ui_get_loans(), get_dashboard_data()

        loan, error = crud.return_book(
            db,
            safe_int(loan_id),
            LoanReturn(
                return_date=date.fromisoformat(return_date)
            )
        )

        if loan is None:
            return error, ui_get_loans(), get_dashboard_data()

        message = f"Book returned successfully. Loan ID={loan.id}"

        return message, ui_get_loans(), get_dashboard_data()

    except ValueError:
        return "Date format must be YYYY-MM-DD. Example: 2026-06-01", ui_get_loans(), get_dashboard_data()

    except Exception as e:
        return f"Error: {str(e)}", ui_get_loans(), get_dashboard_data()

    finally:
        db.close()


# =========================
# CSS
# =========================

custom_css = """
body {
    background: #f5f7fb;
}

.gradio-container {
    max-width: 1280px !important;
    margin: auto !important;
    font-family: Inter, Arial, sans-serif !important;
}

#app-header {
    padding: 28px 32px;
    border-radius: 24px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    margin-bottom: 20px;
}

#app-header h1 {
    font-size: 34px;
    margin-bottom: 8px;
}

#app-header p {
    color: #cbd5e1;
    font-size: 16px;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(160px, 1fr));
    gap: 16px;
    margin: 12px 0 24px 0;
}

.stat-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.stat-card.danger {
    border-color: #fecaca;
    background: #fff7f7;
}

.stat-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 32px;
    font-weight: 800;
    color: #111827;
}

.section-card {
    border: 1px solid #e5e7eb !important;
    border-radius: 20px !important;
    padding: 18px !important;
    background: #ffffff !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04) !important;
}

button {
    border-radius: 12px !important;
    font-weight: 600 !important;
}

textarea, input {
    border-radius: 12px !important;
}

.dataframe {
    border-radius: 16px !important;
    overflow: hidden !important;
}
"""


# =========================
# GRADIO UI
# =========================

with gr.Blocks(
    title="Simple Library Manager",
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="slate",
        secondary_hue="blue",
        neutral_hue="slate"
    )
) as app:

    gr.HTML(
        """
        <div id="app-header">
            <h1>Simple Library Manager</h1>
            <p>Professional mini library system for managing books, readers, loans and overdue records.</p>
        </div>
        """
    )

    dashboard_html = gr.HTML(value=get_dashboard_data())

    with gr.Tab("Dashboard"):
        gr.Markdown("## System Overview")
        refresh_dashboard_btn = gr.Button("Refresh Dashboard")
        refresh_dashboard_btn.click(
            get_dashboard_data,
            inputs=[],
            outputs=dashboard_html
        )

        gr.Markdown(
            """
            ### Project Features

            - Book management: create, read, update, delete
            - Reader management: create, read, update, delete
            - Loan management: create loan and return book
            - Reports: active loans and overdue loans
            - Database: SQLite
            - Backend logic: SQLAlchemy + CRUD layer
            """
        )

    with gr.Tab("Books"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Add New Book")

                    book_title = gr.Textbox(label="Book Title", placeholder="Example: Python Basic")
                    book_author = gr.Textbox(label="Author", placeholder="Example: Kim Minsoo")

                    create_book_btn = gr.Button("Create Book", variant="primary")
                    create_book_msg = gr.Textbox(label="Message", lines=2)

            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Update Book")

                    update_book_id = gr.Number(label="Book ID", precision=0)
                    update_book_title = gr.Textbox(label="New Title")
                    update_book_author = gr.Textbox(label="New Author")
                    update_book_available = gr.Checkbox(label="Is Available", value=True)

                    update_book_btn = gr.Button("Update Book")
                    update_book_msg = gr.Textbox(label="Message", lines=2)

            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Delete Book")

                    delete_book_id = gr.Number(label="Book ID", precision=0)

                    delete_book_btn = gr.Button("Delete Book", variant="stop")
                    delete_book_msg = gr.Textbox(label="Message", lines=2)

        gr.Markdown("### Book List")

        refresh_books_btn = gr.Button("Refresh Books")
        books_table = gr.Dataframe(
            value=ui_get_books(),
            label="Books",
            interactive=False,
            wrap=True
        )

        create_book_btn.click(
            ui_create_book,
            inputs=[book_title, book_author],
            outputs=[create_book_msg, books_table, dashboard_html]
        )

        update_book_btn.click(
            ui_update_book,
            inputs=[
                update_book_id,
                update_book_title,
                update_book_author,
                update_book_available
            ],
            outputs=[update_book_msg, books_table, dashboard_html]
        )

        delete_book_btn.click(
            ui_delete_book,
            inputs=[delete_book_id],
            outputs=[delete_book_msg, books_table, dashboard_html]
        )

        refresh_books_btn.click(
            ui_get_books,
            inputs=[],
            outputs=books_table
        )

    with gr.Tab("Readers"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Add New Reader")

                    reader_name = gr.Textbox(label="Reader Name", placeholder="Example: Dima")
                    reader_phone = gr.Textbox(label="Phone", placeholder="Example: 010-1234-5678")

                    create_reader_btn = gr.Button("Create Reader", variant="primary")
                    create_reader_msg = gr.Textbox(label="Message", lines=2)

            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Update Reader")

                    update_reader_id = gr.Number(label="Reader ID", precision=0)
                    update_reader_name = gr.Textbox(label="New Name")
                    update_reader_phone = gr.Textbox(label="New Phone")

                    update_reader_btn = gr.Button("Update Reader")
                    update_reader_msg = gr.Textbox(label="Message", lines=2)

            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Delete Reader")

                    delete_reader_id = gr.Number(label="Reader ID", precision=0)

                    delete_reader_btn = gr.Button("Delete Reader", variant="stop")
                    delete_reader_msg = gr.Textbox(label="Message", lines=2)

        gr.Markdown("### Reader List")

        refresh_readers_btn = gr.Button("Refresh Readers")
        readers_table = gr.Dataframe(
            value=ui_get_readers(),
            label="Readers",
            interactive=False,
            wrap=True
        )

        create_reader_btn.click(
            ui_create_reader,
            inputs=[reader_name, reader_phone],
            outputs=[create_reader_msg, readers_table, dashboard_html]
        )

        update_reader_btn.click(
            ui_update_reader,
            inputs=[update_reader_id, update_reader_name, update_reader_phone],
            outputs=[update_reader_msg, readers_table, dashboard_html]
        )

        delete_reader_btn.click(
            ui_delete_reader,
            inputs=[delete_reader_id],
            outputs=[delete_reader_msg, readers_table, dashboard_html]
        )

        refresh_readers_btn.click(
            ui_get_readers,
            inputs=[],
            outputs=readers_table
        )

    with gr.Tab("Loans"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Create Loan")

                    loan_book_id = gr.Number(label="Book ID", precision=0)
                    loan_reader_id = gr.Number(label="Reader ID", precision=0)
                    loan_date_input = gr.Textbox(label="Loan Date", placeholder="2026-05-31")
                    due_date_input = gr.Textbox(label="Due Date", placeholder="2026-06-14")

                    create_loan_btn = gr.Button("Create Loan", variant="primary")
                    create_loan_msg = gr.Textbox(label="Message", lines=2)

            with gr.Column(scale=1):
                with gr.Group(elem_classes="section-card"):
                    gr.Markdown("### Return Book")

                    return_loan_id = gr.Number(label="Loan ID", precision=0)
                    return_date_input = gr.Textbox(label="Return Date", placeholder="2026-06-01")

                    return_book_btn = gr.Button("Return Book")
                    return_book_msg = gr.Textbox(label="Message", lines=2)

        gr.Markdown("### Loan List")

        refresh_loans_btn = gr.Button("Refresh Loans")
        loans_table = gr.Dataframe(
            value=ui_get_loans(),
            label="Loans",
            interactive=False,
            wrap=True
        )

        create_loan_btn.click(
            ui_create_loan,
            inputs=[
                loan_book_id,
                loan_reader_id,
                loan_date_input,
                due_date_input
            ],
            outputs=[create_loan_msg, loans_table, dashboard_html]
        )

        return_book_btn.click(
            ui_return_book,
            inputs=[return_loan_id, return_date_input],
            outputs=[return_book_msg, loans_table, dashboard_html]
        )

        refresh_loans_btn.click(
            ui_get_loans,
            inputs=[],
            outputs=loans_table
        )

    with gr.Tab("Reports"):
        gr.Markdown("## Loan Reports")

        with gr.Row():
            refresh_active_btn = gr.Button("Show Active Loans")
            refresh_overdue_btn = gr.Button("Show Overdue Loans")

        with gr.Row():
            active_loans_table = gr.Dataframe(
                value=ui_get_active_loans(),
                label="Active Loans",
                interactive=False,
                wrap=True
            )

        with gr.Row():
            overdue_loans_table = gr.Dataframe(
                value=ui_get_overdue_loans(),
                label="Overdue Loans",
                interactive=False,
                wrap=True
            )

        refresh_active_btn.click(
            ui_get_active_loans,
            inputs=[],
            outputs=active_loans_table
        )

        refresh_overdue_btn.click(
            ui_get_overdue_loans,
            inputs=[],
            outputs=overdue_loans_table
        )


app.launch()