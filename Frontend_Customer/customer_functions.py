from db_config import Customer
from config import CONFIG
import json
import requests

def new_account(user):
    response = requests.post(f"{CONFIG['api']['url']}/customer/register", json=user)
    return response

def check_credentials(user):
    response = requests.post(f"{CONFIG['api']['url']}/customer/login", json=user)
    return response

def display_stock():
    results = requests.get(f"{CONFIG['api']['url']}/stock")
    stock = json.loads(results.text)
    return stock

def get_med_details(medicine_id):
    results = requests.get(f"{CONFIG['api']['url']}/stock/get_one/{medicine_id}")
    stock = json.loads(results.text)
    return stock

def send_order(order):
    response = requests.post(f"{CONFIG['api']['url']}/customer/order", json=order)
    return response

def get_orders(user_id):
    results = requests.get(f"{CONFIG['api']['url']}/customer/myorders/{user_id}")
    orders = json.loads(results.text)
    return orders