total_inventory = 0
failed_entries = 0
total_tax = 0

def get_valid_input():
    user_input = input("Enter stock quantity (or type 'exit' to finish): ")
    if user_input.lower() == 'exit':
        return "quit"
    if user_input.isdigit():
        value = int(user_input)
        if value <= 0:
            print("Please enter a positive whole number.")
            return None
        return value
    else:
        print("Invalid input. Please enter a whole number.")
        return None

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * 0.1
    return tax

def generate_report(total_units, failed_entries):
    print("\n--- Inventory Audit Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

while True:
    value = get_valid_input()
    if value == "quit":
        break
    elif value is None:
        failed_entries += 1
        continue
    else:
        total_inventory = process_delivery(total_inventory, value)
        tax = calculate_tax(value)
        total_tax += tax
        print(f"Current total inventory: {total_inventory} units.")
        print(f"Tax for this entry: {tax:.2f}")

generate_report(total_inventory, failed_entries)
print(f"Total Tax Collected: {total_tax:.2f}")