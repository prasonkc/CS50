import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            global name 
            name = request.form.get("name")
            birthday = request.form.get("birthday").split("/")
        except:
            error = "Some Error occured. Make sure the inputs are correct"
            render_template("index.html", error = error)
        month = birthday[0]
        day = birthday[1]
        
        print(name, month, day)
        
        db.execute("INSERT INTO birthdays (name, month, day) VALUES ((?), (?), (?));", name, month, day)
        
        return redirect("/")
    else:
        names = db.execute("SELECT name, month, day FROM birthdays;")
        print(names)
        return render_template("index.html", names = names)

@app.route("/delete", methods = ["POST"])
def delete():
    db.execute("DELETE FROM birthdays WHERE name = (?);", name)
