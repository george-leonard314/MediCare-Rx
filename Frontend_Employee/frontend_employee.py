from flask import Flask, render_template, request, redirect, url_for, session, flash
from hashlib import sha256
from config import CONFIG
from functools import wraps
import secrets
from pharmacist_functions import *
from admin_functions import *
from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for
from datetime import datetime


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


user_session = {
    "user_id" : " ",
    "username": " ",
    "employee_type": " "
}

def login_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash("You need to log in first", "error")
                return redirect(url_for('login', error_message='You need to log in first.'))
            if user_session['employee_type'] not in roles:
                flash("You don't have permission to access this page", "error")
                return redirect(url_for('dashboard'))  # Redirect to appropriate route
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user={
        'username': request.form.get("username"),
        'password': sha256(request.form.get("password").encode()).hexdigest()
        }

        response = check_credentials_admin(user)
        if response.status_code == 200:
            session['username'] = user["username"]
            global user_session 
            user_session= {
            "user_id" : response.json().get('staff_id'),
            "username": user["username"],
            "employee_type": response.json().get('employee_type')
            }
            if user_session["employee_type"] == '1':
                return redirect("/admin/staff")
            elif user_session["employee_type"] == '2':
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
    "employee_type": " "
    }
    return redirect(url_for('login'))


@app.route("/dashboard", methods=["GET"])
@login_required('1','2')
def dashboard():
    orders = display_pending_orders()
    return render_template("dashboard.html", orders = orders)


@app.route("/dashboard/customers")
@login_required('1','2')
def customer_accounts():
    customers = display_accounts()
    pending_customers = [customer for customer in customers if customer["validation"] == 'Pending']
    return render_template("customer_accounts.html", customers = pending_customers)

@app.route("/dashboard/customers/<int:customer_id>", methods=["POST"])
@login_required('1','2')
def response(customer_id):
    reason = {}
    reason["status"] = request.form.get('status')
    reason["reason"] = request.form.get('reason')

    response_account(customer_id, reason)
    return redirect(url_for('customer_accounts'))

@app.route("/dashboard/orders/<int:order_id>", methods=["GET", "POST"])
@login_required('1','2')
def order(order_id):
    order = get_order(order_id)
    if request.method == "POST":
        reason = {
            "status": request.form.get('status'),
            "reason": request.form.get('reason')
        }
        response_order(order_id, reason)
        # Redirect to the same page or wherever needed after handling the response
        return redirect(url_for('dashboard'))
    return render_template("order_details.html", order=order)

@app.route("/dashboard/orders/<int:order_id>/customer")
@login_required('1','2')
def view_customer(order_id):
    order = get_order(order_id)
    customer_id = order["customer_id"]
    customer_details = get_customer(customer_id)
    return render_template("customer_details.html", customer=customer_details)

@app.route("/dashboard/orders/<int:order_id>/medicine")
@login_required('1','2')
def medicine(order_id):
    order = get_order(order_id)
    medicine_id = order.get("medicine_id")
    medicine_details = get_stock(medicine_id)
    return render_template("medicine_details.html", medicine=medicine_details)


@app.route("/admin/staff")
@login_required('1')
def admin():
    return render_template("dashboard_admin.html", staff=list_of_staff())

@app.route("/admin/staff/add", methods=["GET", "POST"])
@login_required('1')
def new_staff():
    if request.method == "GET":
        return render_template("new_staff.html")
    elif request.method == "POST":
        staff = {}
        staff["full_name"] = request.form["full_name"]
        staff["username"] = request.form["username"]
        staff["password"] = request.form["password"]
        staff["employee_type"] = request.form["employee_type"]
        staff["email"] = request.form["email"]
        staff["phone"] = request.form["phone"]
        staff["employee_id"] = add_staff(staff)
        return render_template("new_staff.html", new_staff = staff)
    
    return make_response("Invalid request", 400)

@app.route("/admin/staff/remove/<int:staff_id>")
@login_required('1')
def removestaff(staff_id):
    remove_staff(staff_id)

    return redirect("/admin/staff")

@app.route("/admin/staff/update/<int:staff_id>", methods=["GET", "POST"])
@login_required('1')
def editstaff(staff_id):
    if request.method == "GET":
        staff = get_staff(staff_id)
        return render_template("edit_staff.html", staff=staff)
    elif request.method == "POST":
        staff = {
            "employee_id": staff_id,
            "full_name": request.form["full_name"],
            "username":  request.form["username"],
            "password":      request.form["password"],
            "employee_type":      request.form["employee_type"],
            "email": request.form["email"],
            "phone": request.form["phone"]
        }
        update_staff(staff_id,staff)
        return render_template("edit_staff.html", staff=staff, staff_updated=staff)
    
    return make_response("Invalid request", 400)


if __name__ == "__main__":
    app.run(host=CONFIG["frontend_employee"]["listen_ip"], port=CONFIG["frontend_employee"]["port"], debug=CONFIG["frontend_employee"]["debug"])
