# Enterprise E-Commerce Order Management System — Common Files

These two files are shared by every team member and should not be duplicated:

- `common/logger.py` — call `get_logger(__name__)` in every module for consistent logging (console + `logs/app.log` + `logs/error.log`).
- `common/database.py` — shared SQLAlchemy `engine`, `Base`, and `get_db_session()`. All models must inherit from this same `Base`.

## Folder structure convention for the team
```
ecommerce_oms/
├── common/
│   ├── __init__.py
│   ├── logger.py
│   └── database.py
├── customer_management/      # Member 1
├── product_management/       # Member 2
├── inventory_management/     # Member 3
├── cart_order_management/    # Member 4
├── payment_delivery/         # Member 5
├── reports_analytics/        # Member 6
├── main.py
└── requirements.txt
```

## How each member uses these files

**Models** (in your own module file):
```python
from common.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
```

**Logging** (in any file):
```python
from common.logger import get_logger
logger = get_logger(__name__)
logger.info("Product added successfully")
```

**Database session** (wherever you read/write data):
```python
from common.database import get_db_session

def add_product(name, price):
    with get_db_session() as session:
        session.add(Product(name=name, price=price))
    # auto-commits, auto-rollback on error, auto-closes
```

**Creating tables** — run once from `main.py`, after importing every
member's model file:
```python
from common.database import init_db
import customer_management.models
import product_management.models
# ...import every member's models module here...
init_db()
```

## Quick test
```
pip install -r requirements.txt
python common/database.py   # creates ecommerce_oms.db and confirms connection
python common/logger.py     # writes a sample log entry to logs/
```