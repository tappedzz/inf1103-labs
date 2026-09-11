total_inventory = 0
failed_entries = 0
while True:
    stock_quantity = input('Enter stock quantity: (or type "exit" to finish): ')
    if stock_quantity.lower() == 'exit':
        break
    if not stock_quantity.isdigit():
        print("Invalid input. Please enter a whole number.")
        failed_entries += 1
        continue
    stock_quantity = int(stock_quantity)
    if stock_quantity < 0:
        print("Invalid input. Please enter a non-negative number.")
        failed_entries += 1
        continue

    total_inventory += stock_quantity

    if total_inventory > 500:
        print("Total inventory exceeds 500 units.")
        break
    else:
        print(f"Current total inventory: {total_inventory} units.")   

print("\n--- Inventory Audit Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")