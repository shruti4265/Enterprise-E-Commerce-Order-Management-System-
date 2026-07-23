from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from sqlalchemy.sql import (
    func
)

from common.database import Base


# -------------------------------------------------
# Stock Transaction Model
# -------------------------------------------------

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
        String(150)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    product = relationship(
        "Product",
        back_populates="stock_transactions"
    )

    def __repr__(self):

        return (
            f"StockTransaction("
            f"transaction_id={self.transaction_id}, "
            f"product_id={self.product_id}, "
            f"change_qty={self.change_qty}, "
            f"transaction_type='{self.transaction_type}', "
            f"reason='{self.reason}'"
            f")"
        )