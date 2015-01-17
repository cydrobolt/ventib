from flask import render_template, redirect, url_for, request, flash, session
from web.utils import auth
from web.database import *
import time

def register_login():
    return render_template("register_login.html")

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
    return render_template("user.html", user=user, texts=user.texts)

def new_text():
    user = User.get(User.api_key == request.form["key"])
    Text.create(user=user, text=request.form["text"], time=time.time(), location=request.form["location"])
    return 'ign: 420/69 would add new text again'
