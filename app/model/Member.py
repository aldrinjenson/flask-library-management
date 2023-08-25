from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String)
    location = db.Column(db.String)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
