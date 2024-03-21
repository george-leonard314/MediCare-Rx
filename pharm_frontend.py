from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for

from config import CONFIG
from student_api_shim import add_student, list_of_students, get_student, update_student, delete_student


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("home.html")