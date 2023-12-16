import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT stock_name, price, cash, no_of_stocks  FROM stocks JOIN users ON users.id = stocks.user_id WHERE user_id = ?", session["user_id"])

    
    for stock in stocks:
        stock['stock_price'] = (lookup(stock['stock_name'])['price'])
        
        
    return render_template("index.html", stocks = stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        buy_symbol = request.form.get("buy")
        no_of_shares = request.form.get("shares")
        values = lookup(buy_symbol)
        
        if not buy_symbol or not values:
            return apology("Incorrect symbol")
        elif not no_of_shares:
            return apology("Enter the number of shares")
        
        
        buy_price = float(values["price"]) * int(no_of_shares)
        cash_amount = int(db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])[0]["cash"])

        if(cash_amount >= buy_price):
            cash_amount = cash_amount - buy_price
            db.execute("UPDATE users SET cash = (?) WHERE id = (?)", cash_amount, session["user_id"])
            
            db.execute("INSERT INTO stocks (user_id, price, stock_name, no_of_stocks) VALUES (?,?,?,?)", session["user_id"], buy_price, values["name"], no_of_shares)
            
            tran = "Buy"
            db.execute("INSERT INTO history (user_id, tran, name) VALUES (?,?,?)", session["user_id"], tran, buy_symbol)
            return redirect("/")

        else:
            return apology("Insufficient price")
            


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM HISTORY WHERE user_id = ?", session["user_id"])
    return render_template("history.html", history = history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
    
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        stocks = lookup(request.form.get("symbol"))
        return render_template("quoted.html", stocks = stocks)
    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if(request.method == "GET"):
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        if not username or not password1:
            return apology("Please provide username and password")
        
        if password1 != password2:
            return apology("Passwords do not match")
        
        password1 = generate_password_hash(password1)
        
        db.execute("INSERT INTO users (username, hash) VALUES ((?), (?))", username, password1)
        
        return render_template("login.html")
        


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute("SELECT stock_name FROM stocks WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks = stocks)
    else:
        sell = request.form.get("selected_stock")
        no_of_shares_sell = int(request.form.get("no_of_shares_sell"))
                
        if not sell or not no_of_shares_sell:
            return apology("No such stock or insuffiecent stocks")
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash_amount = cash[0]['cash']
            profit = float(cash_amount) + (float(lookup(sell)['price']) * no_of_shares_sell)
            
            current_number_owned = db.execute("SELECT no_of_stocks FROM stocks WHERE user_id = ?", session["user_id"])[0]['no_of_stocks']
            

            if current_number_owned == 1:
                db.execute("DELETE FROM stocks WHERE stock_name = ?", sell)
            else:
                db.execute("UPDATE stocks SET no_of_stocks = (?) WHERE stock_name = (?) AND user_id = (?)", current_number_owned - no_of_shares_sell, sell, session["user_id"])
                
            db.execute("UPDATE users SET cash = ? WHERE id = ?", profit, session["user_id"])
            
            tran = "SELL"
            db.execute("INSERT INTO history (user_id, tran, name) VALUES (?,?,?)", session["user_id"], tran, sell)
        
            return redirect("/")
