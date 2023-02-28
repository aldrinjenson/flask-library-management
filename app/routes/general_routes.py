from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404