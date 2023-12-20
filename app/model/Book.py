from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn13 = db.Column(db.String(50), unique=True, nullable=False)
    isbn = db.Column(db.String(50), unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)
    language = db.Column(db.String, default="English")
    publisher = db.Column(db.String, default="")
    rating = db.Column(db.Float, default=5)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    transactions = relationship("Transaction", back_populates="book")

    def __init__(
        self, title, isbn, isbn13, author, rating, publisher, language="English"
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language = language
        self.publisher = publisher
        self.rating = rating
