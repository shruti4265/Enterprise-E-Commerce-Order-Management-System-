from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.database import Base


class StockTransaction(Base):

    __tablename__ = "stock_transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    change_qty = Column(
        Integer,
        nullable=False
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    reason = Column(
        String(150),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    product = relationship(
        "Product",
        back_populates="stock_transactions"
    )