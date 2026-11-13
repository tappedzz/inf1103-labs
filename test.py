from inventory_manager import Inventory, PhysicalProduct, DEFAULT_SUPPLIER

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