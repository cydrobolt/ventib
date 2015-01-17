from flask import render_template

def index():
    return render_template('home.html')

def rlog():
    return render_template('rlog.html')
