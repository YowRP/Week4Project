import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).with_name("inventory.txt")


def load_inventory():
    """Load the saved inventory total and transaction history."""
    if not INVENTORY_FILE.exists():
        return 0, []

    try:
        with INVENTORY_FILE.open("r", encoding="utf-8") as file:
            inventory_data = json.load(file)

        if not isinstance(inventory_data, dict):
            return 0, []

        total_units = inventory_data.get("total_units", 0)
        transaction_history = inventory_data.get("transaction_history", [])

        if not isinstance(total_units, int):
            total_units = 0

        if not isinstance(transaction_history, list):
            transaction_history = []

        return total_units, transaction_history

    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return 0, []


def save_inventory(total_units, transaction_history):
    """Save the inventory total and transaction history to the file."""
    inventory_data = {
        "total_units": total_units,
        "transaction_history": transaction_history,
    }

    with INVENTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(inventory_data, file, indent=4)
        file.write("\n")


def get_valid_input():
    """Ask the user for a valid stock quantity."""
    failed_attempts = 0

    while True:
        user_input = input("Please enter the stock quantity: ").strip()

        if user_input.lower() in ("quit", "q"):
            return None, failed_attempts

        if not user_input.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_attempts += 1
            continue

        return int(user_input), failed_attempts


def process_delivery(current_total, new_value):
    """Add a new delivery amount to the current inventory total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculate 10% tax on the transaction amount."""
    tax_rate = 0.1
    return amount * tax_rate


def generate_report(total_units, deliveries_processed, failed_attempts):
    """Display the final inventory report."""
    print("Total units will be : " + str(total_units))
    print("Deliveries processed : " + str(deliveries_processed))
    print("Failed attempts : " + str(failed_attempts))


def main():
    """Run the inventory tracking program."""
    total_units, transaction_history = load_inventory()
    deliveries_processed = 0
    failed_attempts = 0

    while True:
        user_input, attempts = get_valid_input()
        failed_attempts += attempts

        if user_input is None:
            break

        total_units = process_delivery(total_units, user_input)
        transaction_history.append(user_input)
        calculate_tax(user_input)
        deliveries_processed += 1

    generate_report(total_units, deliveries_processed, failed_attempts)
    save_inventory(total_units, transaction_history)


if __name__ == "__main__":
    main()

