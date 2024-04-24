# TODO CLI for stock management

import argparse
import sys

from config import CONFIG
from pharm_functions import add, delete, read_all, update

def display_stock_list():
    stock = read_all()
    for med in stock:
        print(f"ID: {med['med_id']}   Name: {med['med_name']}     Amount: {med['med_quantity']} stucks     Price:{med['med_price']} euro    Description:{med['med_description']} ")

def main():
    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("-a", "--add", action="store_true")
    operations.add_argument("-l", "--list", action="store_true")
    operations.add_argument("-r", "--remove", action="store_true")
    operations.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-n", "--name")
    parser.add_argument("-q", "--quantity", type=int)
    parser.add_argument("-p", "--price", type=int)
    parser.add_argument("-d", "--description")
    parser.add_argument("--med_id", type=int)  # Added for remove and update operations
    arguments = parser.parse_args()

    if arguments.list:
        display_stock_list()
    
    if arguments.add:
        med = {
            'med_name': arguments.name,
            'med_quantity': arguments.quantity,
            'med_price': arguments.price,
            'med_description': arguments.description
        }
        new_med_id, status_code = add(med)
        print(f"New medicine added with ID: {new_med_id}")
    
    if arguments.remove:
        status_message, status_code = delete(arguments.med_id)
        print(status_message)
    
    if arguments.update:
        med = {
            'medicine_quantity': arguments.quantity
        }
        updated_med = update(arguments.med_id, med)
        print(f"Medicine with ID {arguments.med_id} updated successfully.")

if __name__ == "__main__":
    sys.exit(main())
