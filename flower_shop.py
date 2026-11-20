
import json
import os


TRANSACTION_FILE = "transactions.json"


# DISPLAY AVAILABLE FLOWERS
def display_flowers(flowers):
    print("\n========== AVAILABLE FLOWERS ==========")
    print("-" * 50)
    print(f"{'Code':<10}{'Flower':<15}{'Stock':<10}{'Price':>10}")
    print("-" * 50)

    for flower in flowers:
        print(
            f"{flower['code']:<10}"
            f"{flower['name']:<15}"
            f"{flower['quantity']:<10}"
            f"₱{flower['price']:>9.2f}"
        )

    print("-" * 50)


# ADD FLOWERS TO CART
def add_to_cart(cart, flower, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if quantity > flower["quantity"]:
        raise ValueError("Not enough flowers available in stock.")

    # Check if the flower is already in the cart
    for item in cart:
        if item["code"] == flower["code"]:
            item["quantity"] += quantity
            flower["quantity"] -= quantity
            print("Flower quantity updated in cart.")
            return

    # Create a new cart item
    cart_item = {
        "code": flower["code"],
        "name": flower["name"],
        "quantity": quantity,
        "price": flower["price"]
    }

    cart.append(cart_item)

    # Deduct purchased quantity from inventory
    flower["quantity"] -= quantity

    print(f"{quantity} {flower['name']}(s) added to cart.")


# CALCULATE TOTAL PURCHASE
def calculate_total(cart):
    total = 0

    for item in cart:
        subtotal = item["quantity"] * item["price"]
        total += subtotal

    return total


# GENERATE PURCHASE RECEIPT
def generate_receipt(cart, total):
    print("\n")
    print("=" * 45)
    print("              BLOOMSCAPE")
    print("             FLOWER SHOP")
    print("=" * 45)

    print(f"{'Flower':<15}{'Qty':<5}{'Subtotal':>15}")
    print("-" * 45)

    for item in cart:
        subtotal = item["quantity"] * item["price"]

        print(
            f"{item['name']:<15}"
            f"{item['quantity']:<5}"
            f"₱{subtotal:>14.2f}"
        )

    print("-" * 45)
    print(f"{'TOTAL AMOUNT:':<25}₱{total:>19.2f}")
    print("=" * 45)
    print("       Thank you for your purchase!")
    print("=" * 45)


# SAVE TRANSACTION
def save_transaction(transaction):
    records = load_transactions()

    records.append(transaction)

    with open(TRANSACTION_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)


# LOAD TRANSACTION HISTORY
def load_transactions():
    if not os.path.exists(TRANSACTION_FILE):
        return []

    try:
        with open(TRANSACTION_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)

            if isinstance(records, list):
                return records

            raise ValueError("Invalid transaction file format.")

    except json.JSONDecodeError as error:
        raise ValueError("Transaction file contains invalid JSON.") from error
