import sys
import argparse
import getpass
from stock_functions import add_stock, remove_stock, list_stock, update_stock
from auth import login, logout, is_logged_in

def display_stock_list():
     stock = list_stock()
     for med in stock:
        print(f"ID: {med['medicine_id']}   Name: {med['medicine_name']}   Quantity: {med['medicine_quantity']}   Price: {med['price_stuck']} euro   Description: {med['description']}\n")

def prompt_credentials():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password

def prompt_command():
    command = input("Enter command (add/list/remove/update/logout): ")
    return command

def main():
    if not is_logged_in():
        print("You must log in to use this program.")
        username, password = prompt_credentials()
        login_result = login(username, password)
        print(login_result)
        if "successful" not in login_result:
            return

    while True:
        command = prompt_command()

        if command == "logout":
            print(logout())
            break

        elif command == "list":
            display_stock_list()

        elif command == "add":
            name = input("Enter medicine name: ")
            quantity = int(input("Enter quantity: "))
            price = int(input("Enter price per unit: "))
            description = input("Enter description: ")
            med = {
                'medicine_name': name,
                'medicine_quantity': quantity,
                'price_stuck': price,
                'description': description
            }
            new_med_id = add_stock(med)
            print(f"New medicine added with ID: {new_med_id}")

        elif command == "remove":
            med_id = int(input("Enter medicine ID to remove: "))
            status_message = remove_stock(med_id)
            print(status_message)

        elif command == "update":
            med_id = int(input("Enter medicine ID to update: "))
            name = input("Enter new medicine name: ")
            quantity = int(input("Enter new quantity: "))
            price = int(input("Enter new price per unit: "))
            description = input("Enter new description: ")
            med = {
                'medicine_name': name,
                'medicine_quantity': quantity,
                'price_stuck': price,
                'description': description
            }
            response = update_stock(med_id, med)
            print(f"Medicine with ID {response} updated successfully.")

        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
