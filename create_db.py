import sqlite3
import sys

from config import CONFIG

class ExampleDB:
    @staticmethod
    def initialize(database_connection: sqlite3.Connection):
        cursor = database_connection.cursor()
        try:
            print("Dropping existing tables (if present)...")
            cursor.execute("DROP TABLE course")
            cursor.execute("DROP TABLE student")
            cursor.execute("DROP TABLE grade")
        except sqlite3.OperationalError as db_error:
            print(f"Unable to drop table. Error: {db_error}")
        print("Creating tables...")
        cursor.execute(ExampleDB.CREATE_TABLE_COURSE)
        cursor.execute(ExampleDB.CREATE_TABLE_STUDENT)
        cursor.execute(ExampleDB.CREATE_TABLE_GRADE)
        database_connection.commit()

    #    print("Populating database with sample data...")
    #   cursor.executemany(ExampleDB.INSERT_STUDENT, ExampleDB.sample_students)
    #   cursor.executemany(ExampleDB.INSERT_COURSE, ExampleDB.sample_courses)
    #   cursor.executemany(ExampleDB.INSERT_GRADE, ExampleDB.sample_grades)
    #   database_connection.commit()

    CREATE_TABLE_STUDENT = """
    CREATE TABLE IF NOT EXISTS student (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT
    )
    """

    CREATE_TABLE_COURSE = """
    CREATE TABLE IF NOT EXISTS course (
        course_id TEXT PRIMARY KEY,
        course_name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """

    CREATE_TABLE_GRADE = """
    CREATE TABLE IF NOT EXISTS grade (
        grade_id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        grade REAL NOT NULL,
        student_id INTEGER NOT NULL,
        course_id TEXT NOT NULL,
        FOREIGN KEY (student_id) 
            REFERENCES student(student_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        FOREIGN KEY (course_id)
            REFERENCES course(course_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    )
    """

    INSERT_STUDENT = "INSERT INTO student VALUES (?, ?, ?, ?, ?)"
    INSERT_COURSE = "INSERT INTO course VALUES (?, ?, ?)"
    INSERT_GRADE = "INSERT INTO grade VALUES (?, ?, ?, ?, ?)"

    #sample_students = [
    # (1, "Tim", "Jansma", "t.jansma@fontys.nl", "+31401234567"),
    # (2, "Bart", "Zanden, vd", "bart.vanderzanden@fontys.nl", "+31409012345"),
    #(3, "Stan", "Hartingsveldt", "s.hartingsveldt@fontys.nl", "+31407890123"),
    #(4, "Xuemei", "Pu", "x.pu@fontys.nl", "+31404567890"),
    #(5, "Mehrzad", "Verdizadegan", "m.verdizadegan@fontys.nl", "+31407654321")
    #]

    #sample_courses = [
    #    ("I2CBPR", "Programming for Infrastructure", "Learn to program in Python for Infrastructure student."),
    #    ("I2CBCP", "Connecting & Provisioning", "Roll out stuff and tie it together."),
    #    ("I2CBMS", "Managing & Securing", "Keep it all in control and locked up."),
    #    ("I2CBCS", "Case Study", "Do everything as a team.")
    #]

    #sample_grades = [
    #    (1, "01-09-2023", 9.5, 1, "I2CBPR"),
    #    (2, "01-09-2023", 9.6, 2, "I2CBPR"),
    #    (3, "03-09-2023", 8.5, 1, "I2CBCP"),
    #    (4, "03-09-2023", 9.5, 3, "I2CBCP"),
    #    (5, "02-09-2023", 5.5, 1, "I2CBMS"),
    #    (6, "02-09-2023", 9.5, 5, "I2CBMS"),
    #    (7, "04-09-2023", 9.9, 4, "I2CBCS"),
    #    (8, "04-09-2023", 8.1, 5, "I2CBCS"),
    #    (9, "04-09-2023", 7.5, 1, "I2CBCS"),
    #    (10, "01-09-2023", 9.4, 3, "I2CBPR")
    #]

def main():
    """Execute main function."""
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = sqlite3.Row

    ExampleDB.initialize(db_conn)
    db_conn.close()

    print("Database creation finished!")    

    return 0

# --- Program entry ---
if __name__ == "__main__":
    sys.exit( main() )
