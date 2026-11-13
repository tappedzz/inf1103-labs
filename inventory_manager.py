import json
import time
from abc import ABC, abstractmethod


class Supplier():
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_supplier_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self):
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Contact Email: {self.__contact_email}")

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def update_stock(self, quantity):
        self.__stock = quantity
        print(f"Stock updated successfully for {self.__name}.")

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_product_name(self) -> str:
        return self.__name

    def get_product_price(self) -> float:
        return self.__price

    def get_product_stock(self) -> int:
        return self.__stock
       
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def get_supplier(self) -> Supplier:
        return self.__supplier

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class OrderLine():
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_quantity(self) -> int:
        return self.__quantity

    def get_product(self) -> Product:
        return self.__product

    def calculate_subtotal(self) -> float:
        return self.__product.get_product_price() * self.__quantity

class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def display_order_summary(self) -> None:
        print(f"Order ID: {self.__order_id}")
        print("Order Summary:")
        for order_line in self.__order_lines:
            product = order_line.get_product()
            quantity = order_line.get_quantity()
            subtotal = order_line.calculate_subtotal()
            print(f"Product: {product.get_product_name()} | Quantity: {quantity} | Subtotal: ${subtotal:.2f}")
        total = self.calculate_total()
        print(f"Total Order Amount: ${total:.2f}")


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, product_name: str, product_price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, product_name, product_price, stock, supplier)
        self.__weight: float = weight
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "This product requires Physical Shipping"

    def calculate_shipping_cost(self) -> float:
        if self.__weight >10:
            shipping_price = self.get_product_price() * 0.5
        elif self.__weight > 5:
            shipping_price = self.get_product_price() * 0.2
        else:
            shipping_price = self.get_product_price() * 0.1
        return shipping_price
        

class DigitalProduct(Product):
    def __init__(self, product_id: str, product_name: str, product_price: float, stock: int, downloadsize: int, supplier: Supplier):
        super().__init__(product_id, product_name, product_price, stock, supplier)
        self.__downloadsize: int = downloadsize

    def get_downloadsize(self) -> int:
        return self.__downloadsize
    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__downloadsize} mb")

    def get_fulfilment_info(self) -> str:
        return "This product requires Digital Delivery"


DEFAULT_SUPPLIER = Supplier("SUP001", "Default Supplier", "supplier@exmaple.com")
class Inventory:
    def __init__(self):
        self.__products: dict[str, Product] = {}
    

    def add_product(self, product: Product) -> None:
        if product.get_product_id() in self.__products:
            print(f"Product {product.get_product_id()} is already in inventory")
        else:
            self.__products[product.get_product_id()]=product
            print("Product added successfully!")

    def remove_product(self,product_id:str) -> None:
        if product_id in self.__products:
            del self.__products[product_id]
            print(f"Product {product_id} removed from inventory.")
        else:
            print(f"Product with ID {product_id} not found in inventory.")
    
    def update_stock(self, product_id: str, quantity: int) -> None:
        if product_id not in self.__products:
            print(f"Product with ID {product_id} not found in inventory.")
            return
        product = self.__products[product_id]
        product.update_stock(quantity)
        if product.get_product_stock() <= 0:
            del self.__products[product_id]
            print(f"Product {product_id} removed from inventory due to low stock.")
        

    def search_product(self, product_id:str) -> None:
        if product_id in self.__products:
            self.__products[product_id].display_information()
        else:
            print(f"Product with ID {product_id} not found in inventory.")

    def find_product(self, product_id: str) -> Product | None:
        return self.__products.get(product_id, None)

    def load_inventory(self, filename="inventory.json"):
        try:
            with open(filename, "r") as file:
                data=json.load(file)
                for product_id, info in data.items():
                    if info["type"]=="physical":
                        product = PhysicalProduct(product_id, info["name"], info["price"], info["stock"], info["weight"], DEFAULT_SUPPLIER)
                    else:
                        product = DigitalProduct(product_id, info["name"], info["price"], info["stock"], info["size"], DEFAULT_SUPPLIER)
                    self.__products[product_id] = product
                print(f"{filename} found and loaded successfully")
        except FileNotFoundError:
            print(f"{filename} not found. Starting with empty inventory")
        except json.JSONDecodeError:
            print("Error reading inventory file. Starting with empty inventory")

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
        else:
            print("Current Inventory")
            print("--------------------------------")
            for product in self.__products.values():
                product.display_information()
            print("--------------------------------")
    
    def save_inventory(self, filename="inventory.json"):
        data={}
        for product_id, product in self.__products.items():
            data[product_id]={
                "name": product.get_product_name(),
                "price": product.get_product_price(),
                "stock": product.get_product_stock(),
            }
            if isinstance(product, PhysicalProduct):
                data[product_id]["type"]="physical"
                data[product_id]["weight"]=product.get_weight()
            if isinstance(product,DigitalProduct):
                data[product_id]["type"]="digital"
                data[product_id]["size"]=product.get_downloadsize()


        try:
            with open(filename, "w") as file:
                json.dump(data,file,indent=4)
            print("Saving inventory to json")
            time.sleep(2)
            print("Inventory saved successfully")

        except Exception as e:
            print(f"Error saving : {e}")


if __name__ == "__main__":
    inventory = Inventory()
    inventory.load_inventory()
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
            try:
                phyordigi=input("Is this a Physical or Digital Product? (P/D)")
                if phyordigi.lower()=="p":
                    weight=float(input("Whats the weight of this product? (in kg)"))
                elif phyordigi.lower()=="d":
                    weight=float(input("Whats the size of this product? (in mb)"))
                else:
                    print("Invalid Type")
                    continue
                product_id = input("Enter product ID: ").strip().upper()
                product_name = input("Enter product name: ")
                product_price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Price must be a number and quantity must be a whole number. Product not added.")
                continue
            if phyordigi.lower()=="p":
                    new_product = PhysicalProduct(product_id, product_name, product_price, quantity, weight, DEFAULT_SUPPLIER)
            if phyordigi.lower()=="d":
                    new_product = DigitalProduct(product_id, product_name, product_price, quantity, weight, DEFAULT_SUPPLIER)
            inventory.add_product(new_product)
        elif choice == '2':
            product_id = input("Enter product ID to update: ").strip().upper()
            try:
                quantity = int(input("Enter new quantity: "))
            except ValueError:
                print("Quantity must be a whole number. Stock not updated.")
                continue
            inventory.update_stock(product_id, quantity)
        elif choice == '3':
            search_id = input("Enter Product ID: ").strip().upper()
            inventory.search_product(search_id)
        elif choice == '4':
            inventory.display_all()
        elif choice == '5':
            inventory.save_inventory()
            continue
        elif choice=="6":
            quitorno=input("Are you sure you want to quit? (Y/N)")
            if quitorno.lower()=="y":
                print("The system will now check for any unsaved items and save it.")
                inventory.save_inventory()
                print("Thank You for using our system! See you again!")
                break
            elif quitorno.lower()=="n":
                continue
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")


    