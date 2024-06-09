from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()

class Staff(Base):
    
    #! Declaration for Staff accounts

    __tablename__ = 'staff'
    employee_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    employee_type = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    orders = relationship("Order", back_populates="employee")




class Customer(Base):

    #! Declaration for Customer accounts

    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
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


class Order(Base):

    #! Declaration for Orders

    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('staff.employee_id'), nullable=False)
    date = Column(Date, nullable=False)
    medicine_quantity = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    subtotal = Column(Integer, nullable=False)
    reason_customer = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    reason_employee = Column(Text, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Staff", back_populates="orders")


class Stock(Base):

    #! Delcaration of Stock

    __tablename__ = 'stock'
    medicine_id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_name = Column(String, unique=True, nullable=False)
    medicine_quantity = Column(Integer, nullable=False)
    price_stuck = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)




