from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from db_config import *
from datetime import datetime

Session = sessionmaker(bind=engine)

def register():
    data = request.json

    session = Session()
    try:
        # Check if the username already exists
        existing_user = session.query(Customer).filter_by(username=data["username"]).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409  # Conflict status code
        
        
        new_account = Customer(
            full_name=data["fullname"],
            username=data["username"],
            password=data["password"],
            sex=data["sex"],
            age=data["age"],
            height=data["height"],
            weight=data["weight"],
            email=data["email"],
            phone=data["phone"],
            validation=data["validation"]
        )

        session.add(new_account)
        session.commit()
        new_customer_id = new_account.customer_id
        return jsonify({"customer_id": new_customer_id}), 201
    except:
        session.rollback()
        raise
    finally:
        session.close()

def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    session = Session()
    try:
        customer = session.query(Customer).filter_by(username=username).first()
        if customer and customer.password == password and customer.validation == "approved":
            return jsonify({"customer_id": customer.customer_id}), 200
        else:
            return jsonify({"error": "Invalid username or password, or invalid account"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

def new_order():

    data = request.json

    session = Session()
    try:
        
        new_order = Order(
            medicine_id=data["medicine_id"],
            customer_id=data["customer_id"],
            employee_id=data["employee_id"],
            subtotal=data["subtotal"],
            address=data["address"],
            date= datetime.now(),
            reason_customer=data["reason_customer"],
            medicine_quantity=data["medicine_quantity"],
            reason_employee=data["reason_employee"],
            status=data["status"]
        )

        session.add(new_order)
        session.commit()
        
        ordered_medicine = session.query(Stock).filter_by(medicine_id=data["medicine_id"]).first()
        if ordered_medicine:
            ordered_medicine.medicine_quantity -= data["medicine_quantity"]
            session.commit()
        
        
        new_order_id = new_order.order_id
        return jsonify({"order_id": new_order_id}), 200
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_user_orders(user_id):
    session = Session()
    try:
        # Query orders associated with the user_id
        user_orders = session.query(Order).filter_by(customer_id=user_id).all()
        
        # Create a list to store order details
        orders_list = []
        
        # Iterate through user_orders and format data
        for order in user_orders:
            order_data = {
                "order_id": order.order_id,
                "medicine_id": order.medicine_id,
                "employee_id": order.employee_id,
                "subtotal": order.subtotal,
                "address": order.address,
                "date": order.date.strftime("%Y-%m-%d %H:%M:%S"),  # Format date as string
                "reason_customer": order.reason_customer,
                "medicine_quantity": order.medicine_quantity,
                "reason_employee": order.reason_employee,
                "status": order.status
            }
            orders_list.append(order_data)
        print(orders_list)
        return jsonify(orders_list), 200
    except Exception as e:
        # Handle exceptions and rollback session
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Close the session
        session.close()
    



    