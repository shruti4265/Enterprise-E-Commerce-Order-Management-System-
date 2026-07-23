from sqlalchemy.exc import SQLAlchemyError

from common.database import SessionLocal
from common.logger import logger

from inventory_management.models.inventory import Inventory
from inventory_management.models.stock_transaction import StockTransaction

from inventory_management.validations.inventory_validation import (
    validate_product_id,
    validate_quantity
)


# -------------------------------------------------
# Add Stock
# -------------------------------------------------

def add_stock():

    session = SessionLocal()

    try:

        product_id = int(
            input("Enter Product ID : ")
        )

        quantity = int(
            input("Enter Quantity to Add : ")
        )

        validate_product_id(
            product_id
        )

        validate_quantity(
            quantity
        )

        inventory = session.query(
            Inventory
        ).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:

            print(
                "Inventory record not found."
            )

            return

        inventory.quantity += quantity

        transaction = StockTransaction(
            product_id=product_id,
            change_qty=quantity,
            transaction_type="IN",
            reason="Stock Added"
        )

        session.add(
            transaction
        )

        session.commit()

        logger.info(
            f"Stock added for Product ID : {product_id}"
        )

        print(
            "Stock added successfully."
        )

    except ValueError as exception:

        session.rollback()

        logger.error(
            exception
        )

        print(
            exception
        )

    except SQLAlchemyError as exception:

        session.rollback()

        logger.error(
            exception
        )

        print(
            "Database Error."
        )

    except Exception as exception:

        session.rollback()

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()


# -------------------------------------------------
# Reduce Stock
# -------------------------------------------------

def reduce_stock():

    session = SessionLocal()

    try:

        product_id = int(
            input("Enter Product ID : ")
        )

        quantity = int(
            input("Enter Quantity to Reduce : ")
        )

        validate_product_id(
            product_id
        )

        validate_quantity(
            quantity
        )

        inventory = session.query(
            Inventory
        ).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:

            print(
                "Inventory record not found."
            )

            return

        if inventory.quantity < quantity:

            print(
                "Insufficient Stock."
            )

            return

        inventory.quantity -= quantity

        transaction = StockTransaction(
            product_id=product_id,
            change_qty=-quantity,
            transaction_type="OUT",
            reason="Order Confirmed"
        )

        session.add(
            transaction
        )

        session.commit()

        logger.info(
            f"Stock reduced for Product ID : {product_id}"
        )

        print(
            "Stock reduced successfully."
        )

    except Exception as exception:

        session.rollback()

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()


# -------------------------------------------------
# Check Stock
# -------------------------------------------------

def check_stock():

    session = SessionLocal()

    try:

        product_id = int(
            input("Enter Product ID : ")
        )

        validate_product_id(
            product_id
        )

        inventory = session.query(
            Inventory
        ).filter_by(
            product_id=product_id
        ).first()

        if inventory is None:

            print(
                "Inventory record not found."
            )

            return

        print("\nInventory Details")
        print("-" * 35)

        print(
            f"Product ID : {inventory.product_id}"
        )

        print(
            f"Quantity : {inventory.quantity}"
        )

        print(
            f"Low Stock Threshold : "
            f"{inventory.low_stock_threshold}"
        )

    except Exception as exception:

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()


# -------------------------------------------------
# Display Inventory
# -------------------------------------------------

def display_inventory():

    session = SessionLocal()

    try:

        inventory_list = session.query(
            Inventory
        ).all()

        if len(inventory_list) == 0:

            print(
                "Inventory is empty."
            )

            return

        print("\nInventory Details")
        print("=" * 50)

        for inventory in inventory_list:

            print(
                inventory
            )

    except Exception as exception:

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()


# -------------------------------------------------
# Display Low Stock Products
# -------------------------------------------------

def display_low_stock():

    session = SessionLocal()

    try:

        inventory_list = session.query(
            Inventory
        ).filter(
            Inventory.quantity <=
            Inventory.low_stock_threshold
        ).all()

        if len(inventory_list) == 0:

            print(
                "No Low Stock Products."
            )

            return

        print("\nLow Stock Products")
        print("=" * 50)

        for inventory in inventory_list:

            print(
                inventory
            )

    except Exception as exception:

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()


# -------------------------------------------------
# Stock Transaction History
# -------------------------------------------------

def stock_transaction_history():

    session = SessionLocal()

    try:

        transaction_list = session.query(
            StockTransaction
        ).all()

        if len(transaction_list) == 0:

            print(
                "No Transaction History Found."
            )

            return

        print("\nStock Transaction History")
        print("=" * 60)

        for transaction in transaction_list:

            print(
                transaction
            )

    except Exception as exception:

        logger.error(
            exception
        )

        print(
            exception
        )

    finally:

        session.close()