bank = []
    
def save_inventory(data):
    try:
        file = open("inventory.txt", "a")
        for entry in data:
            line = ",".join(map(str, entry))
            file.write(line + "\n")
        file.close()
        print("Inventory data saved successfully.")
    except Exception as e:
        print(f"Error saving inventory data: {e}")

def get_index_array():
    try:
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()
        return len(lines) + len(bank)

        # for i in range(len(lines)):
        #     entry = lines[i].strip().split(",")
        #     return entry[0]
        #     # print(f"Order {entry[0]}: {entry[1]}, quantity {entry[2]}")
    except Exception as e:
        print(f"Error saving inventory data: {e}")
    
def load_inventory():
    try:
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        for i in range(len(lines)):
            entry = lines[i].strip().split(",")
            print(f"Order {entry[0]}: {entry[1]}, Quantity {entry[2]}")


    except FileNotFoundError:
        file = open("inventory.txt", "w")
        file.close()
        return []
    
def load_bank():

    for i in range(len(bank)):
        entry = bank[i]
        print(f"Order {entry[0]}: {entry[1]}, Quantity {entry[2]}")


    # except FileNotFoundError:
    #     file = open("inventory.txt", "w")
    #     file.close()
    #     return []


def get_valid_input():
    input_name = input("Enter Product Name or quit: ")
    if input_name.lower() == 'quit':
        return "quit"

    input_quantity = input("Enter Quantity or quit: ")
    if input_quantity.lower() == 'quit':
        return "quit"

    elif input_name !="" and input_quantity.isdigit() == True:
        index = get_index_array()
        order_no=index+1
        print(f"\nNew Order Added: \n Order {order_no} - {input_name}, {input_quantity}")
        return [order_no, input_name, input_quantity]
    else:
        return None



while True:
    print("\n Current Orders:")
    load_inventory()
    load_bank()
    user_input = get_valid_input()

    if user_input == "quit":
        print("Exiting the system:")
        save_inventory(bank)
        break
    elif user_input is None:
        continue
    else:
        list_of_entries = user_input
        bank.append(list_of_entries)