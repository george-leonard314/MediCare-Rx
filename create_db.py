import sqlite3
import sys

from config import CONFIG

class ExampleDB:

    #! define class ExampleDB
    
    @staticmethod
    def initialize(database_connection: sqlite3.Connection):
        cursor = database_connection.cursor()
        try:
            print("Dropping existing tables (if present)...")
            cursor.execute("DROP TABLE staff")
            cursor.execute("DROP TABLE customers")
            cursor.execute("DROP TABLE orders")
            cursor.execute("DROP TABLE stock")
        except sqlite3.OperationalError as db_error:
            print(f"Unable to drop table. Error: {db_error}")
        print("Creating tables...")
        cursor.execute(ExampleDB.CREATE_TABLE_STAFF)
        cursor.execute(ExampleDB.CREATE_TABLE_CUSTOMERS)
        cursor.execute(ExampleDB.CREATE_TABLE_ORDERS)
        cursor.execute(ExampleDB.CREATE_TABLE_STOCK)
        
        database_connection.commit()

        print("Populating database with sample data...")
        cursor.executemany(ExampleDB.INSERT_STAFF, ExampleDB.sample_staff)
        cursor.executemany(ExampleDB.INSERT_CUSTOMER, ExampleDB.sample_customers)
        cursor.executemany(ExampleDB.INSERT_ORDER, ExampleDB.sample_orders)
        cursor.executemany(ExampleDB.INSERT_STOCK, ExampleDB.sample_stock)
        database_connection.commit()

    #! Creating the tables

    CREATE_TABLE_STAFF = """
    CREATE TABLE IF NOT EXISTS staff (
        employee_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        employee_type INTEGER NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """

    CREATE_TABLE_CUSTOMERS = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        sex TEXT NOT NULL,
        age INTEGER NOT NULL,
        height INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """


    CREATE_TABLE_ORDERS = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        medicine_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        employee_id TEXT NOT NULL,
        date TEXT NOT NULL,
        medicine_quantity INTEGER NOT NULL,
        address TEXT NOT NULL,
        subtotal INTEGER NOT NULL,
        reason_customer TEXT NOT NULL,
        status TEXT NOT NULL,
        reason_employee TEXT NOT NULL
    )
    """ 
    

    CREATE_TABLE_STOCK = """
    CREATE TABLE IF NOT EXISTS stock (
        medicine_id INTEGER PRIMARY KEY,
        medicine_name TEXT UNIQUE NOT NULL,
        medicine_quantity INTEGER NOT NULL,
        price_stuck INTEGER NOT NULL,
        description TEXT NOT NULL
    )
    """

    #! Initialize the samples

    INSERT_STAFF = "INSERT INTO staff VALUES (?, ?, ?, ?, ?, ?, ?)"
    INSERT_CUSTOMER = "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    INSERT_ORDER = "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    INSERT_STOCK = "INSERT INTO stock VALUES (?, ?, ?, ?, ?)"

    sample_staff = [
        (1, "Michael De Santa", "admin_pharm_518", "root", 1, "michael@gmail.com", "+40123456789"),
        (2, "Franklin Clinton", "pharm_518", "password", 2, "franklin@gmail.com", "+12343213122"),
        (3, "Trevor Philips", "warehouse_518", "password", 3, "trevor@gmail.com", "+12313213312")
    ]

    sample_customers = [
        (0, "Lester Crest", "lester", "1234", "M", "41", 165, 80, "lester@gmail.com", "+1231231321"),
        (1, "Lamar Davis", "lamar", "1234", "M", "31", 181, 95, "lamar@gmail.com", "+12312312321")
    ]

    sample_orders = [
        (0, 0, 0, "", "23-04-2024", 5, "asdadasddsadas", 10, "I have headaches", "pending approval", ""),
        (1, 1, 1, "2", "23-04-2024", 10, "adsadadasad", 30, "My grandma needs them", "rejected", "Cannot do orders for someone else" )
    ]

    sample_stock = [
        (0, "Ibuprofen", 100, 2, "Med for headaches"),
        (1, "Paracetamol", 200, 3, "Med for grandmas")
    ]

def main():

    #! Execute main function

    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = sqlite3.Row

    ExampleDB.initialize(db_conn)
    db_conn.close()

    print("Database creation finished!")    

    return 0

    #! Program entry

if __name__ == "__main__":
    sys.exit( main() )
