from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from db_config import Stock, engine

Session = sessionmaker(bind=engine)

def read_all():
    session = Session()
    try:
        all_stock = session.query(Stock).all()
        resultset = [stock.__dict__ for stock in all_stock]
        for record in resultset:
            record.pop('_sa_instance_state')  # Remove the SQLAlchemy internal state
        print(resultset)
        return jsonify(resultset)
    finally:
        session.close()

def add():
    stock_data = request.json
    print("Stock:", stock_data)  # Add this line to check the value of stock

    new_stock = Stock(
        medicine_name=stock_data["medicine_name"],
        medicine_quantity=stock_data["medicine_quantity"],
        price_stuck=stock_data["price_stuck"],
        description=stock_data["description"]
    )

    session = Session()
    try:
        session.add(new_stock)
        session.commit()
        new_med_id = new_stock.medicine_id
        return new_med_id, 201
    except:
        session.rollback()
        raise
    finally:
        session.close()

def update(medicine_id):
    session = Session()
    stock_data = request.json
    try:
        stock = session.query(Stock).filter_by(medicine_id=medicine_id).first()
        if not stock:
            return "Stock not found", 404
        
        stock.medicine_name = stock_data["medicine_name"]
        stock.medicine_quantity = stock_data["medicine_quantity"]
        stock.price_stuck = stock_data["price_stuck"]
        stock.description = stock_data["description"]

        session.commit()
        return medicine_id
    except:
        session.rollback()
        raise
    finally:
        session.close()

def remove(medicine_id):
    session = Session()
    try:
        stock = session.query(Stock).filter_by(medicine_id=medicine_id).first()
        if not stock:
            return "Stock not found", 404
        
        session.delete(stock)
        session.commit()
        return "Successfully deleted.", 204
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_one(medicine_id):
    session = Session()
    try:
        stock = session.query(Stock).filter_by(medicine_id=medicine_id).first()
        if not stock:
            return jsonify({"error": "Stock not found"}), 404
        
        # Convert the SQLAlchemy object to a dictionary
        stock_dict = stock.__dict__
        stock_dict.pop('_sa_instance_state', None)  # Remove the SQLAlchemy internal state
        print(stock_dict)
        return jsonify(stock_dict), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()