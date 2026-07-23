from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Product

logger = get_logger(__name__)


def disable_product(pid):
    with get_db_session() as session:
        product = session.query(Product).filter_by(product_id=pid).first()
        if product is None:
            print("Product Not Found")
            return

        product.is_active = False
        logger.info("Product disabled: %s", pid)
    print("Product Disabled Successfully")
