from db_config import *
from config import CONFIG
import json
import requests

def check_credentials_admin(user):
    response = requests.post(f"{CONFIG['api']['url']}/admin/login", json=user)
    return response

def get_staff(id):
    result = requests.get( f"{CONFIG['api']['url']}/admin/staff/{id}")
    staff = json.loads(result.text)

    return staff

def add_staff(staff):
    response = requests.post( f"{CONFIG['api']['url']}/admin/staff/add", json=staff )
    
    return response

def remove_staff(id):
    requests.delete( f"{CONFIG['api']['url']}/admin/staff/remove/{id}")

def list_of_staff():
    results = requests.get( f"{CONFIG['api']['url']}/admin/staff")
    staff = json.loads(results.text)

    return staff

def update_staff(id, staff):
    response = requests.put( f"{CONFIG['api']['url']}/admin/staff/update/{id}", json=staff)
    staff = json.loads(response.text)

    return response
