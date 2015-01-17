# Ventib Backend Server
# Being Built at at PennApps XI

from flask import Flask, render_template, request, g, redirect, Markup, url_for, flash, session
import os, sys, string, random
# Init Flask
app = Flask(__name__, static_url_path='/static')
random.seed()

@app.route('/')
def root():
    try:
        if session['username']:
            return render_template("nli_splash.html")
        else:
            return render_template("ili_dash.html")
    except:
        return render_template("nli_splash.html")

app.secret_key = 'lol cat'
