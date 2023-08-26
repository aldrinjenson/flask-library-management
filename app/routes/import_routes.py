from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
import requests
from app import app, db
from app.model.Book import Book
from app.constants import language_map


API_LIMIT = 20


def get_from_api(search_term, page_num=1):
    frappe_api_url = f"https://frappe.io/api/method/frappe-library?title={search_term}&page={page_num}"
    response = requests.get(frappe_api_url)
    if response.status_code == 200:
        books_data = response.json().get("message")

        unique_books_dict = {}  # to skip duplicates of books having same isbn

        for book in books_data:
            isbn13 = book["isbn13"]
            if isbn13 not in unique_books_dict:
                unique_books_dict[isbn13] = book
        unique_books = list(unique_books_dict.values())
        return unique_books
    else:
        return None


def get_books_from_api(search_term, limit):
    limit = int(limit) if limit else 5
    print(limit)

    # ceil
    num_iterations_needed = (limit // API_LIMIT) + 1

    all_books = []
    for i in range(num_iterations_needed):
        books_data = get_from_api(search_term, i + 1)
        all_books += books_data

    return all_books[:limit]


@app.route("/import", methods=["GET", "POST"])
def search_frappe():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        limit = request.form.get("limit")

        matched_books = get_books_from_api(search_term, limit)

        if matched_books and len(matched_books):
            return render_template(
                "books/import.html", books=matched_books, query=search_term
            )
        elif not len(matched_books):
            flash("No books matches your query. Please review and try again.")
        else:
            flash("There seems to be a server error. Please try again after some time.")
        return render_template("books/import.html", books=[])
    else:
        return render_template("books/import.html", books=[])


@app.route("/import/add", methods=["POST"])
def add_to_db():
    search_query = request.form.get("query")
    limit = request.form.get("limit")

    matched_books = get_books_from_api(search_query, limit)

    existing_in_db_with_query = Book.query.filter(
        Book.title.ilike(f"%{search_query}%")
    ).distinct(Book.isbn13)
    existing_isbn13s = set([book.isbn13 for book in existing_in_db_with_query])

    new_books = []
    added_book_count = 0

    existing_book_count = 0
    for book_data in matched_books:
        if book_data["isbn13"] in existing_isbn13s:
            existing_book_count += 1
            continue

        added_book_count += 1
        new_book = Book(
            title=book_data["title"],
            isbn=book_data["isbn"],
            isbn13=book_data["isbn13"],
            author=book_data["authors"],
            language=language_map[book_data["language_code"]],
            publisher=book_data["publisher"],
            rating=float(book_data["average_rating"]),
        )
        new_books.append(new_book)

    try:
        db.session.bulk_save_objects(new_books)
        db.session.commit()
        flash_msg = f"{added_book_count} books added to the database. "
        if existing_book_count:
            flash_msg += f"{existing_book_count} books already present in the database."
        flash(flash_msg)
    except Exception as e:
        db.session.rollback()
        flash("Error adding books to the database", category="error")
        print("Error:", e)
    finally:
        db.session.close()

    return redirect("/books")
