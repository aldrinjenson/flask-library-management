from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


from app.routes import general_routes, book_routes, member_routes

# with app.app_context():
#     print("creating db..")
#     db.create_all()
