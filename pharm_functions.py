import json
import requests

from config import CONFIG

# TODO Functions

def add_stock(med_name, med_quantity, med_price, med_description):
    new_stock = {
        "med_name": med_name,
        "med_quantity": med_quantity,
        "med_price": med_price,
        "med_description": med_description
    }
    response = requests.post(f"{CONFIG['api']['url']}/stock, json=new_med")

def remove_stock(med_id):
    requests.delete(f"{CONFIG['api']['url']}/stock/{med_id}")

def list_stock():
    results = requests.get(f"{CONFIG['api']['url']}/stock")
    stock = json.loads(results.text)

    return stock

def update_stock(med_id, med, med_quantity):
    response = requests.put( f"{CONFIG['api']['url']}/stock/{med['med_id']}", json=med)
    med = json.loads(response.text)

    return int(med["med_id"])