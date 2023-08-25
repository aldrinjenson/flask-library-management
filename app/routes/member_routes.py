from app import app, db
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
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
            date_updated=datetime.utcnow(),
            location=location,
        )
        db.session.add(newMember)
        db.session.commit()
        return redirect("/members")
    else:
        return render_template("member_form.html", member={}, route="add")


@app.route("/members/edit/<int:id>", methods=["GET", "POST"])
def editMember(id):
    selectedMember = Member.query.get_or_404(id)
    print(selectedMember)
    if request.method == "POST":
        try:
            selectedMember.first_name = request.form.get("first_name")
            selectedMember.last_name = request.form.get("last_name")
            selectedMember.email = request.form.get("email")
            selectedMember.language = request.form.get("language", "English")
            selectedMember.username = request.form.get(
                "username",
            )
            selectedMember.location = request.form.get("location")
            selectedMember.date_updated = datetime.utcnow()
            db.session.commit()
            flash("Member Updated successfully !")
        except:
            flash("Error in updating member details. Check server logs!")
        return redirect(url_for("members"))
    else:
        return render_template("member_form.html", member=selectedMember, route="edit")


@app.route("/members/search/", methods=["POST"])
def get_member_search_results():
    query = request.form.get("query", "").lower()

    first_name_matches = Member.query.filter(
        Member.first_name.ilike(f"%{query}%")
    ).all()
    last_name_matches = Member.query.filter(Member.last_name.ilike(f"%{query}%")).all()

    # Combine both lists of matches without duplicates
    filtered_members = list(set(first_name_matches + last_name_matches))

    return render_template("members.html", members=filtered_members)


@app.route("/members/delete/<int:id>", methods=["GET"])
def deleteMember(id):
    selectedMember = Member.query.get_or_404(id)
    print(selectedMember)
    if selectedMember:
        db.session.delete(selectedMember)
        db.session.commit()
        flash("Member deleted successfully.", "success")
    else:
        flash("Member not found.", "danger")
    return redirect("/members")
