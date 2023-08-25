from app import app, db
from flask import Flask, render_template, request, redirect
from app.model.Member import Member


@app.route("/members")
def members():
    members = Member.query.order_by(Member.date_added).all()
    print(members)
    return render_template("members.html", members=members)


@app.route("/members/add/", methods=["GET", "POST"])
def addMembers():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email", "English")
        location = request.form.get("location", 5)
        newMember = Member(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            location=location,
        )
        db.session.add(newMember)
        db.session.commit()
        return redirect("/members")
    else:
        return render_template("member_form.html", member={}, route="add")
