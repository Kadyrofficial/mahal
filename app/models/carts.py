from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum as SqlEnum

from .base import Base
from .shipping import Shipping


if TYPE_CHECKING:
    from .users import User
    from .products import Product

class Cart(Base):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="cart")
    product_count: Mapped[int] = mapped_column(default=0)
    shipping_method: Mapped[Shipping] = mapped_column(SqlEnum(Shipping))
    products: Mapped[list["Product"]] = relationship("Product", back_populates="cart", cascade="all, delete")
