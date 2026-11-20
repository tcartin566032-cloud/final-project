
from flower_shop import (
    display_flowers,
    add_to_cart,
    calculate_total,
    generate_receipt,
    save_transaction,
    load_transactions
)

from datetime import datetime


# FLOWER INVENTORY
flowers = [
    {"code": "F01", "name": "Rose", "quantity": 10, "price": 50.00},
    {"code": "F02", "name": "Tulip", "quantity": 15, "price": 75.00},
    {"code": "F03", "name": "Sunflower", "quantity": 12, "price": 60.00},
    {"code": "F04", "name": "Daisy", "quantity": 20, "price": 35.00},
    {"code": "F05", "name": "Lily", "quantity": 8, "price": 90.00}
]


# TUPLE FOR REQUIRED TRANSACTION FIELDS
TRANSACTION_FIELDS = ("items", "total", "date")


# FIND FLOWER USING ITS UNIQUE CODE
def find_flower(code):
    for flower in flowers:
        if flower["code"].lower() == code.lower():
            return flower

    return None


# DISPLAY MAIN MENU
def display_menu():
    print("\n========== BLOOMSCAPE FLOWER SHOP ==========")
    print("1. View Available Flowers")
    print("2. Purchase Flowers")
    print("3. View Transaction History")
    print("4. Exit")
    print("============================================")


# PURCHASE FLOWERS
def purchase_flowers():
    cart = []

    while True:
        display_flowers(flowers)

        code = input("\nEnter flower code (or 0 to finish): ").strip()

        if code == "0":
            break

        flower = find_flower(code)

        if flower is None:
            print("Invalid flower code. Please try again.")
            continue

        try:
            quantity = int(input("Enter quantity: "))

            add_to_cart(cart, flower, quantity)

        except ValueError as error:
            print("Invalid input:", error)

    if not cart:
        print("\nNo flowers were added to your cart.")
        return

    total = calculate_total(cart)

    # DISPLAY RECEIPT
    generate_receipt(cart, total)

    confirm = input("\nConfirm purchase? (Y/N): ").strip().lower()

    if confirm == "y":

        transaction = {
            "items": cart,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        missing_fields = [
            field for field in TRANSACTION_FIELDS
            if field not in transaction
        ]

        if missing_fields:
            print("Transaction information is incomplete.")

            # Restore inventory
            for item in cart:
                flower = find_flower(item["code"])
                if flower:
                    flower["quantity"] += item["quantity"]

            return

        try:
            save_transaction(transaction)

            print("\nPurchase successful!")
            print("Your receipt is displayed above.")
            print("Transaction saved successfully.")

        except (OSError, ValueError) as error:

            # Restore inventory if saving fails
            for item in cart:
                flower = find_flower(item["code"])

                if flower:
                    flower["quantity"] += item["quantity"]

            print("\nUnable to save transaction:", error)
            print("Stock has been restored.")

    else:

        # RETURN FLOWERS TO INVENTORY
        for item in cart:
            flower = find_flower(item["code"])

            if flower:
                flower["quantity"] += item["quantity"]

        print("\nPurchase cancelled.")
        print("Flowers have been returned to inventory.")


# VIEW TRANSACTION HISTORY
def view_history():
    try:
        records = load_transactions()

    except (OSError, ValueError) as error:
        print("\nUnable to load transaction history:", error)
        return

    print("\n========== TRANSACTION HISTORY ==========")

    if not records:
        print("No previous transactions found.")
        return

    for index, transaction in enumerate(records, start=1):

        print(f"\nTransaction #{index}")
        print("Date:", transaction["date"])

        for item in transaction["items"]:
            subtotal = item["quantity"] * item["price"]

            print(
                f"{item['name']} - "
                f"{item['quantity']} x "
                f"₱{item['price']:.2f} = "
                f"₱{subtotal:.2f}"
            )

        print(f"Total Amount: ₱{transaction['total']:.2f}")
        print("-" * 40)


# MAIN PROGRAM
def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_flowers(flowers)

        elif choice == "2":
            purchase_flowers()

        elif choice == "3":
            view_history()

        elif choice == "4":
            print("\nThank you for visiting Bloomscape!")
            print("Have a wonderful day!")
            break

        else:
            print("\nInvalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
