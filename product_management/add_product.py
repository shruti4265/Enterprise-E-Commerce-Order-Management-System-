from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Category, Inventory, Product

logger = get_logger(__name__)


def add_product(pid, name, category, price, quantity):
    with get_db_session() as session:
        category_record = session.query(Category).filter_by(name=category).first()
        if category_record is None:
            category_record = Category(name=category)
            session.add(category_record)
            session.flush()

        product = Product(
            product_id=pid,
            name=name,
            category=category_record,
            price=price,
            is_active=True,
        )
        product.inventory = Inventory(quantity=quantity)
        session.add(product)
        logger.info("Product added: %s", pid)
    print("Product Added Successfully")
