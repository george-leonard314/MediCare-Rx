from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for
from admin_man_functions import get_staff, add_staff, remove_staff, list_of_staff, update_staff
from config import CONFIG

app = Flask(__name__)

@app.route("/admin/staff")
def homepage():
    return render_template("dashboard.html", staff=list_of_staff())

@app.route("/admin/staff/add", methods=["GET", "POST"])
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
def removestaff(staff_id):
    remove_staff(staff_id)

    return redirect("/admin/staff")

@app.route("/admin/staff/update/<int:staff_id>", methods=["GET", "POST"])
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
