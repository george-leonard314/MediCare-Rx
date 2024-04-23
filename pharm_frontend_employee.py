from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for

from config import CONFIG

app = Flask(__name__)

@app.route("/")
def auth():
    return render_template("employee/login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("employee/dashboard.html")

if __name__ == "__main__":
    app.run(host=CONFIG["frontend-employee"]["listen_ip"], port=CONFIG["frontend-employee"]["port"], debug=CONFIG["frontend-employee"]["debug"])