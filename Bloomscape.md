Document type: Technical Documentation
Course coverage: Weeks 4–5 Python Concepts
Program type: Console-Based Flower Shop Transaction System

## 1. Program Overview
The Flower Shop Transaction System is a Python console program designed for a small flower shop. It allows users to view available flowers, select products, enter purchase quantities, calculate transaction costs, and generate a receipt. It also keeps transaction records in a JSON file.

The program demonstrates the use of Python collections, reusable functions, modules, file handling, and exception handling.

## 2. Problem Description
A small flower shop may experience difficulties managing customer purchases and recording transactions manually. Manual calculations can lead to incorrect totals, while handwritten records can be misplaced or difficult to organize.

The program addresses these problems by organizing flower products in a structured collection, calculating purchase amounts automatically, and saving completed transaction records in a file.

Input: Flower selection and purchase quantity.
Processing: Validate selections, check flower availability, calculate item costs, and compute the total purchase amount.
Output: Available flower list, selected products, transaction receipt, total amount, and saved transaction records.

## 3. Objectives
1. Store multiple flower products using Python collections.
2. Display available flowers and their corresponding prices.
3. Allow customers to select flowers and enter purchase quantities.
4. Calculate the total purchase amount accurately.
5. Generate a summary of completed transactions.
6. Save and retrieve transaction records using file handling.
7. Handle invalid inputs and common program errors.

## 4. Program Requirements and Features
The Flower Shop Transaction System supports displaying available flowers, selecting products, entering quantities, calculating purchase totals, generating receipts, and saving transaction records.

The program assumes that flower names are available in the product list, flower prices are nonnegative, and purchase quantities must be greater than zero. The system also checks flower availability before accepting a purchase.

The transaction file uses JSON text, while Python's standard-library json module handles the conversion of transaction records into a format that can be stored.

**Main Features:**

1. View Flowers – Displays available flowers and their prices.
2. Select Flowers – Allows customers to choose flowers for purchase.
3. Enter Quantity – Accepts the number of flowers the customer wants to buy.
4. Calculate Total – Computes the cost of selected flowers.
5. Display Receipt – Shows the purchase details and total amount.
6. Inventory Management – Displays flower types and their availability.
7. Save Transaction – Stores completed transaction records in a JSON file.

## 5. Program Structure

The program is organized into the following files:

flower_shop_project/
├── main.py
├── flower_shop.py
└── transactions.json    # Created when transactions are saved

- `main.py` contains the main program, menu, and user interaction.
- `flower_shop.py` contains the functions for displaying flowers, processing selections, calculating totals, and handling transaction records.
- `transactions.json` stores completed transaction records between program runs.

```python
from flower_shop import (
    display_flowers,
    add_to_cart,
    calculate_total,
    generate_receipt,
    save_transaction,
    load_transactions
)
```

This separation keeps the main program independent of the transaction operations, making the functions easier to organize, reuse, and test.

## 6. Data Structures Used

### List
A list stores the collection of available flower products. It allows the program to manage multiple flower records.

flowers = []

The list can contain several flower products that customers can select.

### Dictionary
Each flower is stored as a dictionary containing its name, price, and available stock.

```python
flower = {
    "code": "F01",
    "name": "Rose",
    "quantity": 10,
    "price": 50.0
}

flowers.append(flower)
if quantity > flower["quantity"]:
    raise ValueError("Not enough flowers available")
```

A dictionary makes it easier to access flower information using its corresponding keys, such as flower["name"] and flower["price"].

### Tuple
A tuple stores the fixed set of transaction fields supported by the program. It can also be used when checking whether a transaction contains the required information.

```python
TRANSACTION_FIELDS = (
    "flower",
    "quantity",
    "price",
    "total"
)

missing = [
    field for field in TRANSACTION_FIELDS
    if field not in transaction
]
```
A tuple is appropriate because the names of these transaction fields should not change during normal program execution.

## 7. Functions and Responsibilities
The program uses reusable functions to separate its operations into smaller and more manageable tasks.

| Function | Parameters | Returns | Responsibility |
| --- | --- | ---- | --- |
| `display_flowers` | `flowers` | `None` | Displays available flowers and prices |
| `add_to_cart` | `cart, flower, quantity` | `None` | Validates and adds a flower to the cart |
| `calculate_total` | `cart` | `float` | 	Calculates the total purchase amount |
| `generate_receipt` | `cart, total` | `str` | Creates a transaction summary |
| `save_transaction` | `transaction, filename` | `None` | Saves transaction records |
| `load_transactions` | `filename` | `list` | Retrieves previously saved transactions |

```python
def calculate_total(cart):
    total = 0

    for item in cart:
        total += item["quantity"] * item["price"]

    return total
``` 
The function iterates through the selected flowers and multiplies the quantity by the price of each item. It then adds the results to calculate the total purchase amount.

Example: Add to Cart

```python
def add_to_cart(cart, flower, quantity):
    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero"
        )

    if quantity > flower["stock"]:
        raise ValueError(
            "Not enough flowers available"
        )

    item = {
        "name": flower["name"],
        "quantity": quantity,
        "price": flower["price"]
    }

    cart.append(item)
```
This function checks whether the entered quantity is valid and whether enough flowers are available before adding the selected product to the cart.

## 8. File Handling Procedures
The program uses Python's built-in json module to save transaction records in a readable text format. This allows the shop to preserve completed transactions even after the program is closed.

The with statement automatically closes the file after the reading or writing operation is completed.

``` python
import json

def save_transaction(
    transaction,
    filename="transactions.json"
):
    records = load_transactions(filename)
    records.append(transaction)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def load_transactions(filename="transactions.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(
                "Transaction records must be a list"
            )

        return records

    except FileNotFoundError:
        return []
```

- **Write Mode (`w`)** creates or replaces the transaction file with the updated records.
- **Read Mode (`r`)** retrieves previously saved transaction records.
- **json.load()** reads JSON data from the file and converts it into Python objects.
- **json.dump()** converts Python objects into JSON format and writes them into the file.

- UTF-8 Encoding provides consistent text handling when reading and writing files.

- If the transaction file does not exist, the loading function returns an empty list so that new transaction records can be saved.

- If the JSON file contains invalid or corrupted data, json.JSONDecodeError may occur and should be reported or handled separately rather than silently ignored.

## 9. Error Handling
The program uses exception handling to manage common errors that may occur during customer transactions.

Possible errors include invalid numeric input, negative or zero purchase quantities, unavailable flowers, missing transaction files, and malformed JSON data.

The program uses try-except statements to catch errors and display understandable messages to the user.

```python
try:
    quantity = int(input("Enter quantity: "))

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero"
        )

except ValueError as error:
    print("Invalid entry:", error)
```

A ValueError can occur when the customer enters non-numeric text or provides an invalid quantity. The exception allows the program to handle the error without stopping unexpectedly.

Missing transaction files are handled by the load_transactions() function, which returns an empty list when the file is not found.

## 10. Testing, Debugging, and Results
The following table presents test scenarios that can be used to check whether the Flower Shop Transaction System works correctly.

| Test ID | Scenario | Input | Expected result | Example actual result* | Status* |
|---|---|---|---|---|---|
| D01 | Missing colon | `if quantity > 0` | `SyntaxError` | `SyntaxError` | Pass |
| D02 | Incorrect indentation | Misaligned function code | `IndentationError` | `IndentationError` | Pass |
| D03 | Misspelled variable | quanity instead of quantity | `NameError` | `NameError` | Pass |
| D04 | Missing quotation marks | name = Rose | `SyntaxError` | `SyntaxError` | Pass |
| D05 | Incorrect operator | `quantity = 0` in an if condition | `SyntaxError` | `SyntaxError` | Pass |
| D06 | Missing closing parenthesis | print("Total" | `SyntaxError` | `SyntaxError` | Pass |

## Debugging Example (Illustrative)
**Potential defect:** The first implementation of the flower shop program had an incorrect variable name, using quanity instead of quantity.
**Why it was wrong:** The variable name did not match the declared variable, causing a NameError when the program tried to access it.
**Correction:** Change quanity to quantity to make sure the program uses the correct variable name.
Verification: After correcting the spelling, the program successfully accessed the flower quantity and displayed the correct value without producing a NameError.

## 11. Conclusion
The Flower Shop Transaction System demonstrates how Python lists, dictionaries, tuples, functions, modules, file handling, and exception handling can work together in a simple transaction management application.

The program provides a basic solution for organizing flower products, processing customer purchases, calculating transaction totals, and storing completed transaction records. Its use of reusable functions and structured data makes the program easier to maintain and improve.

Possible improvements include adding customer information, searching and deleting previous transactions, generating printable receipts, and expanding the flower inventory.

## 12. References
Python Software Foundation. Python 3 Documentation. https://docs.python.org/3/
Python Software Foundation. Python JSON Documentation. https://docs.python.org/3/library/json.html