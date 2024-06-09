from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request
from db_config import *
import traceback

Session = sessionmaker(bind=engine)


def response_account(customer_id):
    reason = request.json
    session = Session()
    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if customer:
            customer.validation = reason["status"]
            session.commit()
            return jsonify({"message": "Account status updated successfully"}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def display_accounts():
    session = Session()
    try:
        customers = session.query(Customer).all()
        return jsonify([customer.to_dict() for customer in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def display_pending_orders():
    session = Session()
    try:
        orders = session.query(Order).filter_by(status="Pending").all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        error_message = f"Error: {str(e)}, Traceback: {traceback.format_exc()}"
        print(error_message)  # Log the error message to the console
        return jsonify({"error": error_message}), 500
    finally:
        session.close()

def get_customer(customer_id):
    session = Session()
    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if customer:
            return jsonify(customer.to_dict()), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def get_order(order_id):
    session = Session()
    try:
        order = session.query(Order).filter_by(order_id=order_id).first()
        if order:
            return jsonify(order.to_dict()), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def response_order(order_id):
    session = Session()
    reason = request.json

    try:
        order = session.query(Order).filter_by(order_id=order_id).first()
        if order:
            order.status = reason["status"]
            order.reason_employee = reason["reason"]
            session.commit()
            return jsonify({"message": "Order status updated successfully"}), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def remove_account(customer_id):
    session = Session()
    try:
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
            return jsonify({"message": "Customer account removed successfully"}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

