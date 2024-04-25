import sqlite3
from flask import jsonify, request
from config import CONFIG
import sys
from stock_functions import dict_factory, get_db_connection
sys.path.append('/home/g/Programming Asignment/MediCare-Rx')

def read_all():
    ALL_STAFF = "SELECT * FROM staff"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(ALL_STAFF)
    resultset = cursor.fetchall()
    db_conn.close()

    print(resultset)
    return jsonify(resultset)

def add():
    staff = request.json
    print("Employee:", staff)  # Add this line to check the value of stock
    INSERT_STAFF = "INSERT INTO staff (full_name, username, password, employee_type, email, phone) VALUES (?, ?, ?, ?, ?, ?)"
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(INSERT_STAFF, (staff["full_name"], staff["username"], staff["password"], staff["employee_type"], staff["email"], staff["phone"]))
    db_conn.commit()
    new_staff_id = cursor.lastrowid
    db_conn.close()

    return new_staff_id, 201

def update(employee_id):
    staff = request.json
    UPDATE_STAFF = """
    UPDATE staff
    SET full_name = ?,
        username = ?,
        password = ?,
        employee_type = ?,
        email = ?,
        phone = ?
    WHERE employee_id = ?
    """

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(UPDATE_STAFF, (staff["full_name"], staff["username"], staff["password"], staff["employee_type"], staff["email"], staff["phone"], employee_id) )
    db_conn.commit()
    return employee_id

def remove(employee_id):
    DELETE_STAFF = "DELETE FROM staff WHERE employee_id=?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(DELETE_STAFF, (employee_id, ) )
    db_conn.commit()

    return "Succesfully deleted.", 204

def read_one(employee_id):
    GET_STAFF = "SELECT * FROM staff WHERE employee_id = ?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(GET_STAFF, (employee_id, ) )
    resultset = cursor.fetchall()
    db_conn.close()

    if len(resultset) < 1:
        return "Not found", 404
    elif len(resultset) > 2:
        return "Too many results found.", 500

    return jsonify(resultset[0])
