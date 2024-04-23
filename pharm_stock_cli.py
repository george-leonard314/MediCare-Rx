 # TODO CLI for stock management

import argparse
import sys

from config import CONFIG
from pharm_functions import add_stock, remove_stock, list_stock, update_stock

def display_stock_list():
    stock = list_stock()
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
    parser.add_argument("-q", "--quantity")
    parser.add_argument("-p", "--price")
    parser.add_argument("-d", "--description")
    arguments = parser.parse_args()

    if arguments.list:
        display_stock_list()
    
    if arguments.add:
        new_medicine_id = add_stock(arguments.med_name, arguments.med_quantity, arguments.med_price, arguments.med_description)

    if arguments.remove:
        remove_medicine_id = remove_stock(arguments.med_id)
    
    if arguments.update:
        update_medicine_id = update_stock(arguments.med_id, arguments.med_quantity)

if __name__ == "__main__":
    sys.exit( main() )