from sqlalchemy.exc import SQLAlchemyError

from common.database import SessionLocal

from inventory_management.models.inventory import Inventory
from inventory_management.models.stock_transaction import StockTransaction

from inventory_management.validations.inventory_validation import (
    validate_product_id,
    validate_quantity
)

import logging


logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_stock():

    session = SessionLocal()

    try:

        product_id = int(input("Enter Product ID : "))
        quantity = int(input("Enter Quantity to Add : "))

        validate_product_id(product_id)
        validate_quantity(quantity)

        inventory = session.query(Inventory).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:
            print("Inventory record not found.")
            return

        inventory.quantity += quantity

        transaction = StockTransaction(
            product_id=product_id,
            change_qty=quantity,
            transaction_type="IN",
            reason="Stock Added"
        )

        session.add(transaction)

        session.commit()

        logging.info(
            f"Added {quantity} units to Product {product_id}"
        )

        print("Stock added successfully.")

    except Exception as exception:

        session.rollback()

        logging.error(exception)

        print(exception)

    finally:

        session.close()


def reduce_stock():

    session = SessionLocal()

    try:

        product_id = int(input("Enter Product ID : "))
        quantity = int(input("Enter Quantity to Reduce : "))

        validate_product_id(product_id)
        validate_quantity(quantity)

        inventory = session.query(Inventory).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:
            print("Inventory record not found.")
            return

        if inventory.quantity < quantity:
            print("Insufficient stock.")
            return

        inventory.quantity -= quantity

        transaction = StockTransaction(
            product_id=product_id,
            change_qty=-quantity,
            transaction_type="OUT",
            reason="Order Confirmed"
        )

        session.add(transaction)

        session.commit()

        logging.info(
            f"Reduced {quantity} units from Product {product_id}"
        )

        print("Stock reduced successfully.")

    except Exception as exception:

        session.rollback()

        logging.error(exception)

        print(exception)

    finally:

        session.close()


def check_stock():

    session = SessionLocal()

    try:

        product_id = int(input("Enter Product ID : "))

        inventory = session.query(Inventory).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:
            print("Inventory record not found.")
            return

        print("\nCurrent Stock")
        print("----------------------")
        print(f"Product ID : {inventory.product_id}")
        print(f"Quantity   : {inventory.quantity}")

    except Exception as exception:

        print(exception)

    finally:

        session.close()


def display_inventory():

    session = SessionLocal()

    try:

        inventories = session.query(Inventory).all()

        if len(inventories) == 0:
            print("Inventory is empty.")
            return

        print("\n========== Inventory ==========")

        for inventory in inventories:

            print(f"Inventory ID : {inventory.inventory_id}")
            print(f"Product ID   : {inventory.product_id}")
            print(f"Quantity     : {inventory.quantity}")
            print(f"Low Stock    : {inventory.low_stock_threshold}")
            print("-" * 40)

    except Exception as exception:

        print(exception)

    finally:

        session.close()


def display_low_stock():

    session = SessionLocal()

    try:

        inventories = session.query(Inventory).filter(
            Inventory.quantity <= Inventory.low_stock_threshold
        ).all()

        if len(inventories) == 0:
            print("No low stock products.")
            return

        print("\n====== Low Stock Products ======")

        for inventory in inventories:

            print(f"Product ID : {inventory.product_id}")
            print(f"Quantity   : {inventory.quantity}")
            print(f"Threshold  : {inventory.low_stock_threshold}")
            print("-" * 40)

    except Exception as exception:

        print(exception)

    finally:

        session.close()


def stock_transaction_history():

    session = SessionLocal()

    try:

        transactions = session.query(
            StockTransaction
        ).all()

        if len(transactions) == 0:
            print("No transaction history found.")
            return

        print("\n===== Stock Transaction History =====")

        for transaction in transactions:

            print(f"Transaction ID : {transaction.transaction_id}")
            print(f"Product ID     : {transaction.product_id}")
            print(f"Quantity       : {transaction.change_qty}")
            print(f"Type           : {transaction.transaction_type}")
            print(f"Reason         : {transaction.reason}")
            print(f"Date           : {transaction.created_at}")
            print("-" * 50)

    except Exception as exception:

        print(exception)

    finally:

        session.close()