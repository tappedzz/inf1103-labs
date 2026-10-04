import json
import time


def add_product(inventory, product_id, product_name, product_price, quantity):
    inventory[product_id] = {
        "name": product_name,
        "price": product_price,
        "stock": quantity
    }


def load_inventory():
    try:
        file = open("inventory.json", "r")
        inventory = json.load(file)
        file.close()
        print("inventory.json found and loaded successfully.")
        return inventory
    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        print("Error reading inventory file. Starting with empty inventory.")
        return {}


def save_inventory(inventory):
    try:
        with open("inventory.json", "w") as file:
            json.dump(inventory, file, indent=4)
        print("Saving inventory to inventory.json...")
        time.sleep(2)
        print("Inventory saved successfully to inventory.json.")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def update_stock(inventory, product_id, quantity):
    if product_id in inventory:
        inventory[product_id]["stock"] = quantity
        print(f"Stock updated successfully for {inventory[product_id]['name']}.")
        if inventory[product_id]["stock"] <= 0:
            del inventory[product_id]
            print(f"Product ID: {product_id} has been removed from inventory due to low stock.")
    else:
        print(f"Product with ID {product_id} not found in inventory.")


def search_product(inventory, search_id):
    found_product = None
    for product_id, product_info in inventory.items():
        if product_id == search_id:
            found_product = product_info

    if found_product:
        print("Product Found")
        print("--------------------------------")
        print(f"ID: {search_id}")
        print(f"Name: {found_product['name']}")
        print(f"Price: ${found_product['price']:.2f}")
        print(f"Stock: {found_product['stock']}")
        print("--------------------------------")
    else:
        print("Product not found.")


def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
    else:
        print("Current Inventory")
        print("--------------------------------")
        for product_id, product_info in inventory.items():
            print(f"ID: {product_id} | Name: {product_info['name']} | Price: ${product_info['price']:.2f} | Stock: {product_info['stock']}")
        print("--------------------------------")


if __name__ == "__main__":
    inventory = load_inventory()
    while True:
        print("=============================== \n INVENTORY MANAGEMENT SYSTEM \n===============================")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Search Product")
        print("4. Display All Products")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Add New Product")
            product_id = input("Enter product ID: ").strip().upper()
            product_name = input("Enter product name: ")
            try:
                product_price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Price must be a number and quantity must be a whole number. Product not added.")
                continue
            add_product(inventory, product_id, product_name, product_price, quantity)
            print("Product added successfully!")
        elif choice == '2':
            product_id = input("Enter product ID to update: ").strip().upper()
            if product_id not in inventory:
                print("Product not found.")
            else:
                print("Finding Product in Inventory...")
                time.sleep(1)
                print("Product Found!")
                print(f"Product Name: {inventory[product_id]['name']}")
                print(f"Current Stock: {inventory[product_id]['stock']}")
                try:
                    quantity = int(input("Enter new quantity: "))
                except ValueError:
                    print("Quantity must be a whole number. Stock not updated.")
                    continue
                update_stock(inventory, product_id, quantity)
        elif choice == '3':
            search_id = input("Enter Product ID: ").strip().upper()
            search_product(inventory, search_id)
        elif choice == '4':
            display_all(inventory)
        elif choice == '5':
            save_inventory(inventory)
        elif choice == '6':
            save_inventory(inventory)
            print("Exiting Inventory Management System.")
            break
        else:
            print("Invalid choice. Please try again.")