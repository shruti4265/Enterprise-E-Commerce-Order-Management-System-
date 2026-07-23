from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Category, Product

logger = get_logger(__name__)


def update_product(pid, name, category, quantity):
    with get_db_session() as session:
        product = session.query(Product).filter_by(product_id=pid).first()
        if product is None:
            print("Product Not Found")
            return

        category_record = session.query(Category).filter_by(name=category).first()
        if category_record is None:
            category_record = Category(name=category)
            session.add(category_record)
            session.flush()

        product.name = name
        product.category = category_record
        product.inventory.quantity = quantity
        logger.info("Product updated: %s", pid)
    print("Product Updated Successfully")
