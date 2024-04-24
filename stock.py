import sqlite3

from flask import jsonify

from config import CONFIG

def dict_factory(cursor, row):
    fields = [ column[0] for column in cursor.description]
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

    return jsonify(resultset)

def add(med):
    INSERT_STOCK = "INSERT INTO stock (medicine_name, medicine_quantity, price_stuck, description) VALUES (?, ?, ?, ?)"    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(INSERT_STOCK, (med["med_name"], med["med_quantity"], med["med_price"], med["med_description"]))
    db_conn.commit()
    new_med_id = cursor.lastrowid
    db_conn.close()
    
    return new_med_id, 201

def read_one(med_id):
    GET_STOCK = "SELECT * FROM stock where medicine_id = ?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(GET_STOCK, (med_id, ) )
    resultset = cursor.fetchall()
    db_conn.close()

    if len(resultset) < 1:
        return "Not found", 404
    elif len(resultset) > 2:
        return "Too many results found.", 500

    return jsonify(resultset[0])

def update(med_id, med, med_quantity):
    UPDATE_MED = """
    UPDATE stock
    SET medicine_quantity = ?
    WHERE medicine_id = ?
    """

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(UPDATE_MED, (med["medicine_quantity"], med_id) )
    db_conn.commit()

    return read_one(med_id)

def delete(med_id):
    DELETE_STOCK = "DELETE FROM stock WHERE medicine_id=?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(DELETE_STOCK, (med_id, ) )
    db_conn.commit()

    return "Succesfully deleted.", 204
