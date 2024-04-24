import sys
sys.path.append('/home/g/Programming Asignment/MediCare-Rx again/flaskProject')
import argparse
import sys
from config import CONFIG
from stock_manager_functions import add_stock, remove_stock, list_stock,update_stock

def display_stock_list():
    stock = list_stock()
    for med in stock:
        print(f"ID: {med['medicine_id']}   Name: {med['medicine_name']}     Amount: {med['medicine_quantity']} stucks     Price:{med['price_stuck']} euro    Description:{med['description']} \n")

def main():
    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("-a", "--add", action="store_true")
    operations.add_argument("-l", "--list", action="store_true")
    operations.add_argument("-r", "--remove", action="store_true")
    operations.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-i", "--id", type=int)
    parser.add_argument("-n", "--name")
    parser.add_argument("-q", "--quantity", type=int)
    parser.add_argument("-p", "--price", type=int)
    parser.add_argument("-d", "--description")
    arguments = parser.parse_args()

    if arguments.list:
        display_stock_list()
    
    if arguments.add:
        med = {
            'medicine_name': arguments.name,
            'medicine_quantity': arguments.quantity,
            'price_stuck': arguments.price,
            'description': arguments.description
        }
        new_med_id = add_stock(med)
        print(f"New medicine added with ID: {new_med_id}")
    
    if arguments.remove:
        status_message = remove_stock(arguments.id)
        print(status_message)
    
    if arguments.update:
        med = {
            'medicine_name': arguments.name,
            'medicine_quantity': arguments.quantity,
            'price_stuck': arguments.price,
            'description': arguments.description 
        }
        response = update_stock(arguments.id, med)
        print(f"Medicine with ID {response} updated successfully.")

if __name__ == "__main__":
    sys.exit(main())
