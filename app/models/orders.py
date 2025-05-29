from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum as SqlEnum
from enum import Enum

from .base import Base
from .shipping import Shipping


if TYPE_CHECKING:
    from .users import User
    from .products import Product


class OrderStatus(str, Enum):
    active = "active"
    checked = "checked"
    started = "started"
    ordered = "ordered"
    in_china = "in_china"
    in_ashgabad = "in_ashgabad"
    success = "success"
    declined = "declined"


class Order(Base):
    __tablename__ = "orders"

    total: Mapped[int] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="orders")
    product_count: Mapped[int] = mapped_column(default=0)
    shipping_method: Mapped[Shipping] = mapped_column(SqlEnum(Shipping))
    products: Mapped[list["Product"]] = relationship("Product", back_populates="order", cascade="all, delete")
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus))
