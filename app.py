from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


# with app.app_context():
#     db.create_all()


@app.route('/')
def index():
    return render_template('index.html')
