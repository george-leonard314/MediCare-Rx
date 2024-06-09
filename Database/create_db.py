import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import CONFIG
from datetime import datetime
from db_config import *


class ExampleDB:

    @staticmethod
    def initialize(engine):
        print("Dropping existing tables (if present)...")
        Base.metadata.drop_all(engine)

        print("Creating tables...")
        Base.metadata.create_all(engine)

        print("Populating database with sample data...")
        Session = sessionmaker(bind=engine)
        session = Session()

        session.bulk_save_objects([
            Staff(employee_id=1, full_name="Michael De Santa", username="admin_pharm_518", password="4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2", employee_type=1, email="michael@gmail.com", phone="+40123456789"),
            Staff(employee_id=2, full_name="Franklin Clinton", username="pharm_518", password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", employee_type=2, email="franklin@gmail.com", phone="+12343213122"),
            Staff(employee_id=3, full_name="Trevor Philips", username="warehouse_518", password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", employee_type=3, email="trevor@gmail.com", phone="+12313213312"),
            Customer(customer_id=0, full_name="Lester Crest", username="lester", password="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", sex="M", age=41, height=165, weight=80, email="lester@gmail.com", phone="+1231231321", validation="approved"),
            Customer(customer_id=1, full_name="Lamar Davis", username="lamar", password="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", sex="M", age=31, height=181, weight=95, email="lamar@gmail.com", phone="+12312312321", validation="approved"),
            Order(order_id=0, medicine_id=0, customer_id=0, employee_id=1, date=datetime.strptime("2024-04-23", "%Y-%m-%d"), medicine_quantity=5, address="asdadasddsadas", subtotal=10, reason_customer="I have headaches", status="approved", reason_employee="Good Luck!"),
            Order(order_id=1, medicine_id=1, customer_id=1, employee_id=2, date=datetime.strptime("2024-04-23", "%Y-%m-%d"), medicine_quantity=10, address="adsadadasad", subtotal=30, reason_customer="My grandma needs them", status="rejected", reason_employee="Cannot do orders for someone else"),
            Stock(medicine_id=0, medicine_name="Ibuprofen", medicine_quantity=100, price_stuck=2, description="Med for headaches"),
            Stock(medicine_id=1, medicine_name="Paracetamol", medicine_quantity=200, price_stuck=3, description="Med for grandmas")
        ])

        session.commit()
        session.close()

def main():
    # Set up the database connection
    engine = create_engine(CONFIG["database"]["url"])

    # Initialize the database
    ExampleDB.initialize(engine)

    print("Database creation finished!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
