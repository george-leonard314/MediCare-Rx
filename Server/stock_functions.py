import sqlite3
from flask import jsonify, request
from config import CONFIG
import sys
sys.path.append('/home/g/Programming Asignment/MediCare-Rx')

def dict_factory(cursor, row):
    fields = [ column[0] for column in cursor.description ]
    return {key: value for key, value in zip(fields, row)}

def get_db_connection():
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = dict_factory
    return db_conn

def read_all():
    ALL_STOCK = "SELECT * FROM stock"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(ALL_STOCK)
    resultset = cursor.fetchall()
    db_conn.close()

    print(resultset)
    return jsonify(resultset)


def add():
    stock = request.json
    print("Stock:", stock)  # Add this line to check the value of stock
    INSERT_STOCK = "INSERT INTO stock (medicine_name, medicine_quantity, price_stuck, description) VALUES (?, ?, ?, ?)"
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(INSERT_STOCK, (stock["medicine_name"], stock["medicine_quantity"], stock["price_stuck"], stock["description"]))
    db_conn.commit()
    new_med_id = cursor.lastrowid
    db_conn.close()
    
    return new_med_id, 201

def update(medicine_id, stock):
    UPDATE_MEDICINE = """
    UPDATE stock
    SET medicine_name = ?,
        medicine_quantity = ?,
        price_stuck = ?,
        description = ?
    WHERE medicine_id = ?
    """

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(UPDATE_MEDICINE, (stock["medicine_name"], stock["medicine_quantity"], stock["price_stuck"], stock["description"], medicine_id) )
    db_conn.commit()

    return medicine_id


def remove(medicine_id):
    DELETE_MED = "DELETE FROM stock WHERE medicine_id=?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(DELETE_MED, (medicine_id, ) )
    db_conn.commit()

    return "Succesfully deleted.", 204