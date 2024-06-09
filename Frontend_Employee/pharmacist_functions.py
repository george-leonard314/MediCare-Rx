from db_config import *
from config import CONFIG
import json
import requests

def response_account(customer_id, reason):
    response = requests.post(f"{CONFIG['api']['url']}/pharmacist/{customer_id}", json=reason)
    return response

def display_accounts():
    results = requests.get(f"{CONFIG['api']['url']}/pharmacist/pending-customers")
    accounts = json.loads(results.text)
    return accounts

def display_pending_orders():
    results = requests.get(f"{CONFIG['api']['url']}/pharmacist/pending-orders")
    orders = json.loads(results.text)
    return orders

def get_customer(customer_id):
    results = requests.get(f"{CONFIG['api']['url']}/pharmacist/customer/{customer_id}")
    account = json.loads(results.text)
    return account

def get_order(order_id):
    results = requests.get(f"{CONFIG['api']['url']}/pharmacist/order/{order_id}")
    order = json.loads(results.text)
    return order

def remove_account(customer_id):
    response = requests.post(f"{CONFIG['api']['url']}/pharmacist/customer/remove/{customer_id}")
    return response

def response_order(order_id, reason):
    response = requests.post(f"{CONFIG['api']['url']}/pharmacist/order/respond/{order_id}", json=reason)
    return response

def get_stock(medicine_id):
    results = requests.get(f"{CONFIG['api']['url']}/stock/get_one/{medicine_id}")
    stock = json.loads(results.text)
    return stock

