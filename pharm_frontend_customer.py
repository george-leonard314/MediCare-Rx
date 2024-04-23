from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for

from config import CONFIG

app = Flask(__name__)

@app.route("/")
def auth():
    return render_template("customer/login.html")

@app.route("/register")
def register_menu():
    return render_template("customer/register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("customer/dashboard.html")

if __name__ == "__main__":
    app.run(host=CONFIG["frontend-customer"]["listen_ip"], port=CONFIG["frontend-customer"]["port"], debug=CONFIG["frontend-customer"]["debug"])