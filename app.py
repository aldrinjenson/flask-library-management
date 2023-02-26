from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    language = db.Column(db.String, default="English")
    quantity = db.Column(db.Integer, default=1)
    rating = db.Column(db.Float, default=5)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self,
                 title,
                 isbn,
                 author,
                 rating,
                 language="English",
                 quantity=1):
        self.title = title
        self.isbn = isbn
        self.language = language
        self.quantity = quantity
        self.rating = rating
        self.author = author


# with app.app_context():
#     db.create_all()


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/books/search/', methods=["POST"])
def getSearchResults():
    print(request.form)
    query = request.form['query'].lower()
    queryType = request.form['type']
    sqlQuery = Book.title.ilike(f'%{query}%')
    if queryType == 'author':
        sqlQuery = Book.author.ilike(f'%{query}%')

    print(sqlQuery)
    filteredBooks = Book.query.filter(sqlQuery).all()
    return render_template('books.html', books=filteredBooks)


@app.route("/books/")
def books():
    books = Book.query.order_by(Book.date_added).all()
    print(books)
    return render_template('books.html', books=books)


@app.route('/books/add/', methods=["GET", "POST"])
def addBooks():
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        author = request.form.get('author')
        language = request.form.get('language', 'English')
        quantity = request.form.get('quantity', 1)
        rating = request.form.get('rating', 5)
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
        return redirect('/books')
    else:
        return render_template('book_form.html', book={}, route="/add")


@app.route('/books/edit/<int:id>')
def editBook(id):
    selectedBook = Book.query.get_or_404(id)
    print(selectedBook)
    if request.method == "POST":
        try:
            selectedBook.title = request.form.get('title')
            selectedBook.isbn = request.form.get('isbn')
            selectedBook.author = request.form.get('author')
            selectedBook.language = request.form.get('language', 'English')
            selectedBook.quantity = request.form.get('quantity', 1)
            selectedBook.rating = request.form.get('rating', 5)
            db.session.commit()
            return "Book Updated successfully !"
        except:
            return "Error in updating book details. Check server logs!"
    else:
        return render_template('book_form.html',
                               book=selectedBook,
                               route="/edit")
