INVENTORY_FILE = "inventory.txt"

def load_orders():
    """Load previously saved orders, or start empty if the file doesn't exist."""
    orders = []
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            order_id = int(parts[0])
            product_name = parts[1]
            quantity = int(parts[2])
            orders.append((order_id, product_name, quantity))
    except FileNotFoundError:
        orders = []
    return orders

def display_orders(orders):
    """Print all current orders."""
    print("Current Orders:\n")
    for order_id, product_name, quantity in orders:
        print(str(order_id) + ", " + product_name + ", " + str(quantity))
    print()


def get_valid_input(orders):
    """Ask the user for a new product name and quantity."""
    product_name = input("Enter Product Name: ").strip()

    if product_name.lower() in ("quit", "q"):
        return None

    quantity_input = input("Enter Quantity: ").strip()
    if not quantity_input.isdigit():
        print("Invalid input. Please enter a valid number.")
        return get_valid_input(orders)

    order_id = get_next_id(orders)
    return order_id, product_name, int(quantity_input)

def get_next_id(orders):
    """Work out the next order ID, continuing from the last one saved."""
    if len(orders) == 0:
        return 1001
    last_order = orders[-1]
    return last_order[0] + 1


def main():
    """Run the order tracking program."""
    orders = load_orders()
    display_orders(orders)

    while True:
        new_order = get_valid_input(orders)
        if new_order is None:
            break

        orders.append(new_order)
        print("\nNew Order Added:")
        print(str(new_order[0]) + "," + new_order[1] + "," + str(new_order[2]) + "\n")

    save_orders(orders)
    print("Order successfully saved to inventory.txt")


if __name__ == "__main__":
    main()