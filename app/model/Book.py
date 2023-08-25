from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    language = db.Column(db.String, default="English")
    quantity = db.Column(db.Integer, default=1)
    rating = db.Column(db.Float, default=5)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    transactions = relationship("Transaction", back_populates="book")

    def __init__(self, title, isbn, author, rating, language="English", quantity=1):
        self.title = title
        self.isbn = isbn
        self.language = language
        self.quantity = quantity
        self.rating = rating
        self.author = author
