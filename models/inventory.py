from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    inventory_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        unique=True,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    low_stock_threshold = Column(
        Integer,
        nullable=False,
        default=10
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    product = relationship(
        "Product",
        back_populates="inventory"
    )