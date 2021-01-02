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
db = SQL("sqlite:///store.db")


@app.route("/")
@login_required
def index():
    #Show products
    products = db.execute("SELECT * FROM products WHERE amount != 0")
    for i in products:
        i["price"] = usd(i["price"])
    return render_template("index.html", products = products)


@app.route("/funds", methods=["GET", "POST"])
@login_required
def funds():
    if request.method == "GET":
        user = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        user[0]["cash"] = usd(user[0]["cash"])

        return render_template("funds.html", user = user)

    else:
        cash = float(request.form.get("funds"))
        if not cash:
            return apology("Must provide cash", 403)

        check = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        if float(check[0]["cash"]) < (-1 * cash):
            return apology("Negative funds", 403)

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = check[0]["cash"] + cash, id = session["user_id"])

        return redirect("/funds")


@app.route("/buy", methods=["POST"])
@login_required
def buy():
    products = db.execute("SELECT * FROM products WHERE id IN (?) ORDER BY price, name", session["cart"])
    user = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
    price = db.execute("SELECT SUM(price) FROM cart WHERE user_id = :user_id", user_id = session["user_id"])
    amount = db.execute("SELECT amount FROM cart WHERE user_id = :user_id ORDER BY price, name", user_id = session["user_id"])

    if float(user[0]["cash"]) < float(price[0]["SUM(price)"]):
        return apology("Not enough cash", 403)

    for i in range(len(products)):
        db.execute("UPDATE products SET amount = :amount WHERE id = :id", amount = products[i]["amount"] - amount[i]["amount"], id = products[i]["id"])

    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=user[0]["cash"] - price[0]["SUM(price)"], id=session["user_id"])
    db.execute("DELETE FROM cart WHERE user_id = :user_id", user_id = session["user_id"])
    session["cart"].clear()

    return redirect ("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid e-mail and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["name"]

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        #Look for empty information
        session["check"] = ["name", "email", "password", "cpassword"]
        for i in session["check"]:
            if not request.form.get(i):
                return apology(f"must provide {i}", 403)

        #Check if password = password confirmation
        if request.form.get("password") != request.form.get("cpassword"):
            return apology("passwords don't match", 403)

        #Check if e-mail is available
        row = db.execute("SELECT email FROM users")
        for i in row:
            if i == request.form.get("email"):
                return apology("e-mail already registered", 403)

        #Add data to database
        name = request.form.get("name")
        email = request.form.get("email")
        hash_password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (name, email, hash) VALUES (:name, :email, :hash)", name = name, email = email, hash = hash_password)

        return redirect("/login")


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    #Check if cart exists
    if "cart" not in session:
        session["cart"] = []

    #Show products in cart
    if request.method == "GET":

        products = db.execute("SELECT * FROM cart WHERE product_id IN (?)", session["cart"])
        for i in products:
            i["price"] = usd(i["price"])

        return render_template("cart.html", products=products)

    #Add products to the cart
    else:
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
            products = db.execute("SELECT * FROM products WHERE id IN (?)", id)
            cart = db.execute("SELECT * FROM cart WHERE user_id = :user_id AND product_id = :id", id = id, user_id = session["user_id"])

            if not cart:
                db.execute("INSERT INTO cart(product_id, user_id, price, category, name, amount) VALUES (?, ?, ?, ?, ?, ?)",
                            id, session["user_id"], products[0]["price"], products[0]["category"], products[0]["name"], 1)

            else:
                db.execute("UPDATE cart SET amount = :amount, price = :price WHERE product_id = :product_id AND user_id = :user_id",
                    amount = session["cart"].count(id), price = products[0]["price"] * session["cart"].count(id), product_id = id, user_id = session["user_id"])

        return redirect("/cart")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

