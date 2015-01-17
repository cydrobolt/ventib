from flask import render_template, redirect, url_for, request, flash, session, jsonify
from web.utils import auth, core_stats
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

def logout():
    session["username"] = False
    return redirect("/")

def user():
    user = User.get(User.username == session["username"])
    stats = core_stats.CoreStats(user.texts, user.timezone)
    stat_functions = (
            ("Swear words", stats.foul_words_stats(), "red darken-4"),
            ("Sentences spoken", stats.general_stats_total_sentences(), "blue darken-4"),
            ("Markov chain", stats.markov_chains(), "orange darken-4"),
            ("Most common words", stats.most_common_word(), "yellow darken-4"),
            ("Most common time", stats.most_common_time(), "purple darken-4"),
            ("Markov chain", stats.markov_chains(), "green darken-4"),
    )
    return render_template("user.html", stats=stat_functions, user=user)

def new_text():
    user = User.get(User.api_key == request.form["key"])
    for i in request.form["text"].split(","):
        Text.create(user=user, text=i.strip(), time=time.time(), location=request.form["location"])
    return 'ign: 420/69 would add new text again'

def search_text():
    query = request.args["q"]
    u = User.get(User.username == session["username"])
    return jsonify(texts=[i.text for i in list(Text.select().where(Text.user == u, Text.text % ("%%%s%%" % query)))])
