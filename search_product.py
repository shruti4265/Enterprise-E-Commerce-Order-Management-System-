from common.database import get_db_session
from common.logger import get_logger
from product_management.models import Product

logger = get_logger(__name__)


def search_product(category):
	with get_db_session() as session:
		products = (
			session.query(Product)
			.join(Product.category)
			.filter(Product.category.has(name=category))
			.all()
		)

		if not products:
			print("No Products Found")
			return

		for product in products:
			print(
				product.product_id,
				product.name,
				product.category.name,
				product.price,
				product.inventory.quantity if product.inventory else 0,
				"Available" if product.is_active else "Unavailable",
			)
		logger.info("Products searched by category: %s", category)


def search_by_category(category):
	return search_product(category)
