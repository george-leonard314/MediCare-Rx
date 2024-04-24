import sys
sys.path.append('/home/g/Programming Asignment/MediCare-Rx')
from config import CONFIG
import json
import requests
import sys

def add_stock(med):
    response = requests.post(f"{CONFIG['api']['url']}/stock/add", json=med)
    return response
   

def remove_stock(med_id):
    response = requests.delete(f"{CONFIG['api']['url']}/stock/remove/{med_id}")
    return response

def list_stock():
    results = requests.get(f"{CONFIG['api']['url']}/stock")
    stock = json.loads(results.text)
    return stock

def update_stock(med_id, med):
    response = requests.put( f"{CONFIG['api']['url']}/stock/update/{med_id}", json=med)
    med = json.loads(response.text)

    return med