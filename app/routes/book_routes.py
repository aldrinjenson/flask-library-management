from flask import Flask, render_template, request, redirect, flash, url_for
from app import app, db
from app.model.Book import Book
from app.model.Member import Member
from app.utils import get_more_book_details
from sqlalchemy.orm.attributes import instance_dict


@app.route("/books/")
def books():
    books = Book.query.order_by(Book.date_added).all()
    print(books)
    return render_template("books/list.html", books=books)


@app.route("/books/search/", methods=["POST"])
def searchBooks():
    query = request.form["query"].lower()
    queryType = request.form["type"]
    sqlQuery = Book.title.ilike(f"%{query}%")
    if queryType == "author":
        sqlQuery = Book.author.ilike(f"%{query}%")

    print(sqlQuery)
    filteredBooks = Book.query.filter(sqlQuery).all()
    return render_template("books/list.html", books=filteredBooks)


@app.route("/books/add/", methods=["GET", "POST"])
def addBooks():
    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        isbn13 = request.form.get("isbn13")
        author = request.form.get("author")
        language = request.form.get("language", "English")
        publisher = request.form.get("publisher")
        rating = request.form.get("rating", 5)
        newBook = Book(
            title=title,
            isbn=isbn,
            isbn13=isbn13,
            author=author,
            language=language,
            publisher=publisher,
            rating=rating or 5,
        )
        db.session.add(newBook)
        db.session.commit()
        return redirect("/books")
    else:
        return render_template("books/form.html", book={}, route="add")


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def editBook(id):
    selectedBook = Book.query.get_or_404(id)
    print(selectedBook)
    if request.method == "POST":
        try:
            selectedBook.title = request.form.get("title")
            selectedBook.isbn = request.form.get("isbn")
            selectedBook.isbn13 = request.form.get("isbn13")
            selectedBook.author = request.form.get("author")
            selectedBook.language = request.form.get("language", "English")
            selectedBook.publisher = request.form.get("publisher")
            selectedBook.rating = request.form.get("rating", 5)
            db.session.commit()
            flash("Book Updated successfully")
        except:
            flash("Error in updating book details. Check server logs!")
        return redirect(url_for("books"))
    else:
        return render_template("books/form.html", book=selectedBook, route="edit")


@app.route("/books/delete/<int:id>", methods=["GET"])
def deleteBook(id):
    selectedBook = Book.query.get_or_404(id)
    print(selectedBook)
    if selectedBook:
        db.session.delete(selectedBook)
        db.session.commit()
        flash("Book deleted successfully.", "success")
    else:
        flash("Invalid Book id to delete!", "danger")
    return redirect("/books")


@app.route("/books/details/<int:id>")
def getBookDetails(id):
    selectedBook = Book.query.get_or_404(id)

    available_members = Member.query.with_entities(
        Member.id, Member.first_name, Member.last_name
    ).all()

    if selectedBook:
        extra_details = get_more_book_details(selectedBook.isbn)
        selected_book_dict = instance_dict(selectedBook)

        full_book = {**selected_book_dict, **extra_details}
        return render_template(
            "/books/details.html", book=full_book, members=available_members
        )
    else:
        return redirect("/404.html")
