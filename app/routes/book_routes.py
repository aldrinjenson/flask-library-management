from app import app, db
from flask import Flask, render_template, request, redirect, flash, url_for
from app.model.Book import Book


@app.route("/books/")
def books():
    books = Book.query.order_by(Book.date_added).all()
    print(books)
    return render_template("books.html", books=books)


@app.route("/books/search/", methods=["POST"])
def getSearchResults():
    query = request.form["query"].lower()
    queryType = request.form["type"]
    sqlQuery = Book.title.ilike(f"%{query}%")
    if queryType == "author":
        sqlQuery = Book.author.ilike(f"%{query}%")

    print(sqlQuery)
    filteredBooks = Book.query.filter(sqlQuery).all()
    return render_template("books.html", books=filteredBooks)


@app.route("/books/add/", methods=["GET", "POST"])
def addBooks():
    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        author = request.form.get("author")
        language = request.form.get("language", "English")
        quantity = request.form.get("quantity", 1)
        rating = request.form.get("rating", 5)
        newBook = Book(
            title=title,
            isbn=isbn,
            author=author,
            language=language,
            quantity=quantity,
            rating=rating or 5,
        )
        db.session.add(newBook)
        db.session.commit()
        return redirect("/books")
    else:
        return render_template("book_form.html", book={}, route="add")


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def editBook(id):
    selectedBook = Book.query.get_or_404(id)
    print(selectedBook)
    if request.method == "POST":
        try:
            selectedBook.title = request.form.get("title")
            selectedBook.isbn = request.form.get("isbn")
            selectedBook.author = request.form.get("author")
            selectedBook.language = request.form.get("language", "English")
            selectedBook.quantity = request.form.get("quantity", 1)
            selectedBook.rating = request.form.get("rating", 5)
            db.session.commit()
            flash("Book Updated successfully")
        except:
            flash("Error in updating book details. Check server logs!")
        return redirect(url_for("books"))
    else:
        return render_template("book_form.html", book=selectedBook, route="edit")


@app.route("/books/delete/<int:id>", methods=["GET"])
def deleteBook(id):
    selectedBook = Book.query.get_or_404(id)
    print(selectedBook)
    return render_template("book_form.html", book=selectedBook)
