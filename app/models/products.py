from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Enum as SqlEnum, ForeignKey
from typing import TYPE_CHECKING
from enum import Enum

from .base import Base


if TYPE_CHECKING:
    from .carts import Cart
    from .orders import Order


class ProductStatus(str, Enum):
    deactive = "deactive"
    checking_price = "checking_price"


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(default=1)
    status: Mapped[ProductStatus] = mapped_column(SqlEnum(ProductStatus), nullable=False, default=ProductStatus.deactive)

    tracking_number: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=True)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="products")
    
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=True)
    order: Mapped["Order"] = relationship("Order", back_populates="products")
    
    __table_args__ = (
        CheckConstraint("quantity >= 1", name="quantity_min_check"),
    )
