from flask import Flask, render_template, request, redirect, url_for, session, flash
from hashlib import sha256
from config import CONFIG
from functools import wraps
import secrets
from customer_functions import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


user_session = {
    "user_id" : " ",
    "username": " "
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to log in first", "error")
            return redirect(url_for('login', error_message='You need to log in first.'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user={
        'username': request.form.get("username"),
        'password': sha256(request.form.get("password").encode()).hexdigest()
        }

        response = check_credentials(user)
        if response.status_code == 200:
            session['username'] = user["username"]
            global user_session 
            user_session= {
            "user_id" : response.json().get('customer_id'),
            "username": user["username"]
            }
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    global user_session 
    user_session= {
    "user_id" : " ",
    "fullname": " ",
    "username": " "
    }
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = {
            'fullname': request.form.get("fullname"),
            'username': request.form.get("username"),
            'password': sha256(request.form.get("password").encode()).hexdigest(),
            'sex': request.form.get("sex"),
            'age': int(request.form.get("age")),
            'height': int(request.form.get("height")),
            'weight': int(request.form.get("weight")),
            'email': request.form.get("email"),
            'phone': request.form.get("phone"),
            'validation': "Pending"
        }

        response = new_account(user)
        if response.status_code == 201:
            flash('Registration waiting for approval, you will be contacted soon.', 'success')
            return redirect(url_for('login', message='Registration successful'))
        else:
            print("Error")
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    username = user_session["username"]
    available_stock = display_stock()
    return render_template("dashboard.html", username = username, available_stock=available_stock)

@app.route("/order/<int:medicine_id>", methods=["GET", "POST"])
@login_required
def order(medicine_id):
    
    medicine = get_med_details(medicine_id)
    
    if request.method == "POST":

        price = medicine["price_stuck"]
        medicine_quantity = int(request.form.get("quantity"))
        subtotal = price * medicine_quantity

        date_str = datetime.now().isoformat()
        date_obj = datetime.fromisoformat(date_str)
        date_only = date_obj.date()

        order = {
        'medicine_id': medicine_id,
        'customer_id': user_session["user_id"],
        'employee_id': -1,
        'subtotal': subtotal,
        'address': request.form.get("address"),
        'reason_customer': request.form.get("reason"),
        'medicine_quantity': medicine_quantity,
        'reason_employee': "",
        'status': "Pending"
        }

        response = send_order(order)    

        if response.status_code == 200:
            flash("Order processed, you can check the status of your order in the My Order section.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Something went wrong")
    
    return render_template("order.html", medicine=medicine)

@app.route("/dashboard/myorders")
@login_required
def myorder():
    orders = get_orders(user_session["user_id"])
    medicine = display_stock()
    return render_template("myorders.html", orders=orders, medicine=medicine)

if __name__ == "__main__":
    app.run(host=CONFIG["frontend-customer"]["listen_ip"], port=CONFIG["frontend-customer"]["port"], debug=CONFIG["frontend-customer"]["debug"])
