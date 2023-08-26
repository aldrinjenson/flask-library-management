from app import app, db
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import datetime, timedelta
from app.model.Transaction import Transaction


@app.route("/transactions")
def get_transactions():
    transactions = Transaction.query.all()
    return render_template("transactions/list.html", transactions=transactions)


@app.route("/transaction/add", methods=["POST"])
def add_transaction():
    member_id = request.form.get("member")
    book_id = request.form.get("bookId")

    issue_date = datetime.utcnow().date()
    due_date = issue_date + timedelta(days=7)

    new_transaction = Transaction(
        member_id=member_id,
        book_id=book_id,
        issue_date=issue_date,
        due_date=due_date,
        return_date=None,
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
        flash("Transaction added successfully")
    except Exception as e:
        db.session.rollback()
        flash("Error adding transaction", category="error")
        print("Error:", e)
    finally:
        db.session.close()

    return redirect("/books")  # Redirect to a suitable route


@app.route("/transactions/return", methods=["POST"])
def return_book():
    member_id = request.form.get("member_id")
    book_id = request.form.get("book_id")

    transaction = Transaction.query.filter_by(
        member_id=member_id, book_id=book_id, return_date=None
    ).first()

    if transaction:
        transaction.return_date = datetime.utcnow()
        db.session.commit()
        flash("Book returned successfully")
    else:
        flash("Transaction not found or book already returned", category="error")
    return redirect("/transactions")  # Redirect to a suitable route
