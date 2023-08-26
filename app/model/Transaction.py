from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship

from app import db


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = Column(db.Integer, primary_key=True)
    member_id = Column(db.Integer, ForeignKey("members.id"))
    book_id = Column(db.Integer, ForeignKey("books.id"))
    issue_date = Column(db.Date, server_default=text("CURRENT_DATE"))
    due_date = Column(db.Date)
    return_date = Column(db.Date, default=None)

    member = relationship("Member", back_populates="transactions")
    book = relationship("Book", back_populates="transactions")

    def __init__(self, member_id, book_id, issue_date, due_date, return_date):
        self.member_id = member_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = self.return_date
