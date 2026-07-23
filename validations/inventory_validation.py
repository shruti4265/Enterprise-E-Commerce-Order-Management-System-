# -------------------------------------------------
# Inventory Validation Functions
# -------------------------------------------------


def validate_product_id(product_id):

    if product_id <= 0:

        raise ValueError(
            "Product ID must be greater than zero."
        )


def validate_quantity(quantity):

    if quantity <= 0:

        raise ValueError(
            "Quantity must be greater than zero."
        )


def validate_low_stock_threshold(low_stock_threshold):

    if low_stock_threshold < 0:

        raise ValueError(
            "Low Stock Threshold cannot be negative."
        )