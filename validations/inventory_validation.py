def validate_quantity(quantity):

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero."
        )


def validate_low_stock_threshold(threshold):

    if threshold < 0:
        raise ValueError(
            "Low stock threshold cannot be negative."
        )


def validate_product_id(product_id):

    if product_id <= 0:
        raise ValueError(
            "Invalid Product ID."
        )