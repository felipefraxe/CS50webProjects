import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    for row in db.execute("SELECT * FROM stocks WHERE id = :id", id = session["user_id"]):
        quotes = lookup(row["symbol"])
        db.execute("UPDATE stocks SET price = :price, total = :total WHERE name = :name", price = quotes["price"], total = quotes["price"] * row["shares"], name = quotes["name"])
        
    x = db.execute("SELECT SUM(total) FROM stocks WHERE id = :id", id = session["user_id"])
    stocks = db.execute("SELECT * FROM stocks JOIN users ON users.id = stocks.id WHERE stocks.id = :id", id = session["user_id"])
    
    for row in stocks:
        row["price"] = usd(row["price"])
        row["total"] = usd(row["total"])
    stocks[0]["values"] = usd(x[0]["SUM(total)"] + stocks[0]["cash"])
    stocks[0]["cash"] = usd(stocks[0]["cash"])
    
    return render_template("index.html", stocks = stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        shares = int(request.form.get("shares"))
        quotes = lookup(request.form.get("symbol"))
        cost = shares * quotes["price"]

        if not quotes:
            apology("Invalid symbol", 403)

        user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        if user[0]["cash"] < cost:
            return apology("Not enough cash", 403)

        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=user[0]["cash"] - cost, id=session["user_id"])
            rows = db.execute("SELECT * FROM stocks WHERE id = :id AND name = :name", id = session["user_id"], name = quotes["name"])
            
            if len(rows) != 1:
                db.execute("INSERT INTO stocks (id, name, symbol, shares, price, total) VALUES (:id, :name, :symbol, :shares, :price, :total)",
                id=session["user_id"], name=quotes["name"], symbol=quotes["symbol"], shares=shares, price=quotes["price"], total=cost)
                
            else:
                db.execute("UPDATE stocks SET shares = :shares, price = :price, total = :total WHERE id = :id AND name = :name",
                id=session["user_id"], name=quotes["name"], shares = rows[0]["shares"] + shares, price = quotes["price"], total=(rows[0]["shares"] + shares) * quotes["price"])
                
            db.execute("INSERT INTO transactions (id, symbol, shares, price, transacted) VALUES (:id, :symbol, :shares, :price, :transacted)",
            id = session["user_id"], symbol = quotes["symbol"], shares = shares, price = quotes["price"], transacted = datetime.now())
            
            return redirect ("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transactions WHERE id = :id", id = session["user_id"])
    for c in rows:
        c["price"] = usd(c["price"])
        
    return render_template("history.html", rows=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Must provide a valid symbol", 403)
        quote["price"] = usd(quote["price"])

        return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        """Error Checking"""
        if not request.form.get("username"):
            return apology("Must provide Username", 403)

        if not request.form.get("password"):
            return apology("Must provide Password", 403)

        if request.form.get("password") != request.form.get("cpassword"):
            return apology("Passwords don´t match", 403)

        """Adding Data to Database"""
        username = request.form.get("username")
        if len(db.execute("SELECT * FROM users WHERE username = :username", username=username)) == 1:
            return apology("Username already exists", 403)

        else:
            hash_password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash_password)
            db.execute("INTERT INTO stocks (username) VALUES :username", username=username)

        return redirect("/login")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        rows = db.execute("SELECT * FROM stocks WHERE id = :id", id = session["user_id"])
        return render_template("sell.html", rows=rows)
    
    else:
        shares = int(request.form.get("shares"))
        quotes = lookup(request.form.get("symbol"))
        income = shares * quotes["price"]
        
        rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        check = db.execute("SELECT * FROM stocks WHERE id = :id AND name = :name", id = session["user_id"], name = quotes["name"])
        if int(check[0]["shares"]) < shares:
            return apology("Not enough shares", 403)
        
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = rows[0]["cash"] + income, id = session["user_id"])
        db.execute("UPDATE stocks SET shares = :shares, total = :total, price = :price WHERE name = :name AND id = :id",
        shares = check[0]["shares"] - shares, total = (check[0]["total"] - (shares * quotes["price"])), price = quotes["price"], name = quotes["name"], id = session["user_id"])
        
        db.execute("INSERT INTO transactions (id, symbol, shares, price, transacted) VALUES (:id, :symbol, :shares, :price, :transacted)",
            id = session["user_id"], symbol = quotes["symbol"], shares = -1 * shares, price = quotes["price"], transacted = datetime.now())
            
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
