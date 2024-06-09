from flask import jsonify, request
from db_config import Session, Staff

def read_all():
    session = Session()
    resultset = session.query(Staff).all()
    session.close()
    return jsonify([staff.to_dict() for staff in resultset])

def add():
    staff = request.json
    print("Employee:", staff)
    
    new_staff = Staff(
        full_name=staff["full_name"],
        username=staff["username"],
        password=staff["password"],
        employee_type=staff["employee_type"],
        email=staff["email"],
        phone=staff["phone"]
    )
    
    session = Session()
    session.add(new_staff)
    session.commit()
    new_staff_id = new_staff.employee_id
    session.close()
    
    return new_staff_id, 201

def update(employee_id):
    staff = request.json
    
    session = Session()
    existing_staff = session.query(Staff).filter_by(employee_id=employee_id).first()
    
    if not existing_staff:
        return "Not found", 404
    
    existing_staff.full_name = staff["full_name"]
    existing_staff.username = staff["username"]
    existing_staff.password = staff["password"]
    existing_staff.employee_type = staff["employee_type"]
    existing_staff.email = staff["email"]
    existing_staff.phone = staff["phone"]
    
    session.commit()
    session.close()
    
    return employee_id

def remove(employee_id):
    session = Session()
    staff = session.query(Staff).filter_by(employee_id=employee_id).first()
    
    if not staff:
        return "Not found", 404
    
    session.delete(staff)
    session.commit()
    session.close()
    
    return "Successfully deleted.", 204

def read_one(employee_id):
    session = Session()
    staff = session.query(Staff).filter_by(employee_id=employee_id).all()
    session.close()
    
    if len(staff) < 1:
        return "Not found", 404
    elif len(staff) > 1:
        return "Too many results found.", 500
    
    return jsonify(staff[0].to_dict())

def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    session = Session()
    try:
        staff = session.query(Staff).filter_by(username=username).first()
        if staff and staff.password == password:
            return jsonify({"staff_id": staff.employee_id, "employee_type": staff.employee_type}), 200
        else:
            return jsonify({"error": "Invalid username or password, or invalid account"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()