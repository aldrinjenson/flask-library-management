from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os.path import exists
import os

load_dotenv()

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = os.environ.get("SECRET_KEY") or "some_secret_password"  # temporary
db.init_app(app)

# to prevent circular import🙂
from app.routes import (
    general_routes,
    book_routes,
    member_routes,
    transaction_routes,
    import_routes,
)


with app.app_context():
    if not exists("instance/project.db"):
        db.create_all()
        print("Database created.")
    else:
        print("Database present.")
