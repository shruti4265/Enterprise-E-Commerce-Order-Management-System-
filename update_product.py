from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Category, Inventory, Product

logger = get_logger(__name__)


def update_product(product_id, product_name, category, quantity):
	with get_db_session() as session:
		product = session.query(Product).filter_by(product_id=product_id).first()
		if product is None:
			print("Product Not Found")
			return

		category_record = session.query(Category).filter_by(name=category).first()
		if category_record is None:
			category_record = Category(name=category)
			session.add(category_record)
			session.flush()

		product.name = product_name
		product.category = category_record
		if product.inventory is None:
			product.inventory = Inventory(quantity=quantity)
		else:
			product.inventory.quantity = quantity
		logger.info("Product updated: %s", product_id)
	print("Product Updated Successfully")
