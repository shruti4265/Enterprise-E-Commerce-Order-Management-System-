from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Product

logger = get_logger(__name__)


def manage_price(product_id, new_price):
    with get_db_session() as session:
        product = session.query(Product).filter_by(product_id=product_id).first()
        if product is None:
            print("Product Not Found")
            return

        product.price = new_price
        logger.info("Product price updated: %s", product_id)
    print("Price Updated Successfully")


def update_price(product_id, new_price):
    return manage_price(product_id, new_price)
