from flask import Flask, render_template, request, redirect, flash, url_for
from app import app, db
from app.model.Book import Book
import requests


API_LIMIT = 20


def get_from_api(search_term, page_num=1):
    frappe_api_url = f"https://frappe.io/api/method/frappe-library?title={search_term}&page={page_num}"
    response = requests.get(frappe_api_url)
    if response.status_code == 200:
        books_data = response.json().get("message")
        return books_data
    else:
        return None


def get_books_from_api(search_term, limit=5):
    print(limit)

    # ceil
    num_iterations_needed = (limit // API_LIMIT) + 1
    print(num_iterations_needed)

    all_books = []
    for i in range(num_iterations_needed):
        books_data = get_from_api(search_term, i + 1)
        return books_data[:limit]
        # if not books_data:
        #     return None
        # elif not len(books_data):
        #     return []

        all_books.append(books_data)
        if len(all_books) > API_LIMIT:
            return all_books[:limit]
        else:
            return all_books[:limit]

    else:
        return None


@app.route("/import", methods=["GET", "POST"])
def search_frappe():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        limit = int(request.form.get("limit") or 10)

        matched_books = get_books_from_api(search_term, limit)
        print("matched books")
        print(matched_books)

        if matched_books and len(matched_books):
            return render_template("books/import.html", books=matched_books)
        elif not len(matched_books):
            flash("No books matches your query. Please review and try again.")
        else:
            flash("There seems to be a server error. Please try again after some time.")
        return render_template("books/import.html", books=[])
    else:
        return render_template("books/import.html", books=[])


@app.route("/import/add")
def add_to_db():
    pass
