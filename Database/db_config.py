from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import CONFIG
from datetime import datetime


Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    employee_type = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    orders = relationship("Order", back_populates="employee", cascade="all, delete")
    
    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'full_name': self.full_name,
            'username': self.username,
            'password': self.password,
            'employee_type': self.employee_type,
            'email': self.email,
            'phone': self.phone
        }


class Customer(Base):
    #! Declaration for Customer accounts

    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    orders = relationship("Order", back_populates="customer")
    validation = Column(String, nullable=False)

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'full_name': self.full_name,
            'username': self.username,
            'password': self.password,
            'sex': self.sex,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'email': self.email,
            'phone': self.phone,
            'validation': self.validation

        }


class Order(Base):


    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)
    employee_id = Column(Integer, ForeignKey('staff.employee_id'), nullable=True)
    date = Column(Date, nullable=False)
    medicine_quantity = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    subtotal = Column(Integer, nullable=False)
    reason_customer = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    reason_employee = Column(Text, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Staff", back_populates="orders")

    def to_dict(self):
        # Fetch the medicine name from the Stock table based on medicine_id
        session = Session()
        try:
            medicine_name = session.query(Stock.medicine_name).filter_by(medicine_id=self.medicine_id).scalar()
        finally:
            session.close()

        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "medicine_id": self.medicine_id,
            "medicine_name": medicine_name,
            "quantity": self.medicine_quantity, 
            "order_date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "status": self.status,
            "reason_employee": self.reason_employee
        }



class Stock(Base):

    #! Delcaration of Stock

    __tablename__ = 'stock'
    medicine_id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_name = Column(String, unique=True, nullable=False)
    medicine_quantity = Column(Integer, nullable=False)
    price_stuck = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


engine = create_engine(CONFIG["database"]["url"])

Session = sessionmaker(bind=engine)


