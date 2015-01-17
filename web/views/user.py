from flask import render_template, redirect, url_for, request, flash, session
from web.utils import auth

def register_login():
    return render_templates("register_login.html")

def register():
    auth.create_user(request.form["username"], request.form["password"])
    flash("User registered!")
    return redirect(url_for("register_login"))

def login():
    user = auth.authenticate_user(request.form["username"], request.form["password"])
    if not user:
        flash("Wrong!")
        return redirect(url_for("register_login"))
    session["username"] = user.username
    return redirect(url_for("user"))

def user():
    user = User.get(User.username == session["username"])
    return render_template("user.html", user=user)
