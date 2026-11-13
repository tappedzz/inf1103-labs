from inventory_manager import (
    Supplier, Inventory, Product, PhysicalProduct, DigitalProduct, Order, DEFAULT_SUPPLIER
)

print("=== Section 2.2 Association ===")
supplier = Supplier("S002", "TechSupplies", "sales@techsupplies.com")
laptop = PhysicalProduct("P001", "Laptop", 1200, 5, 2.5, supplier)
ebook_a = DigitalProduct("P002", "E-book", 15, 100, 4.2, supplier)

laptop.get_supplier().display_information()
ebook_a.get_supplier().display_information()

del supplier
laptop.get_supplier().display_information()
ebook_a.get_supplier().display_information()

print("\n=== Section 3 Aggregation ===")

mouse = PhysicalProduct("P003", "Mouse", 25, 40, 0.2, DEFAULT_SUPPLIER)

inv_a = Inventory()
inv_b = Inventory()

inv_a.add_product(mouse)
inv_a.remove_product("P003")
mouse.display_information()

inv_b.add_product(mouse)
inv_b.display_all()

print(inv_a.find_product("P003"))             # None
print(inv_b.find_product("P003") is mouse)    # True

print("\n=== Section 4.3 Composition ===")
keyboard = PhysicalProduct("P004", "Keyboard", 60, 15, 0.8, DEFAULT_SUPPLIER)

order1 = Order("O001")
order2 = Order("O002")

order1.add_order_line(mouse, 2)
order1.add_order_line(keyboard, 1)
order2.add_order_line(mouse, 5)

order1.display_order_summary()
print()
order2.display_order_summary()

print(f"\nO001 has {len(order1.get_order_lines())} lines")
print(f"O002 has {len(order2.get_order_lines())} lines")

line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("line1 is line2:", line1 is line2)
print("line1.get_product() is line2.get_product():",
      line1.get_product() is line2.get_product())


print("\n=== Section 6.2 LSP ===")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


ebook = DigitalProduct("D001", "Python E-Book", 15, 100, 50, DEFAULT_SUPPLIER)

show_product_details(mouse) 
print()
show_product_details(ebook)


print("\n=== Section 7.2 Polymorphism ===")

inv = Inventory()
inv.add_product(mouse)
inv.add_product(ebook)

for product in inv.get_products():
    product.display_information()
    print(product.get_fulfilment_info())
    print()
