from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SqlEnum
from typing import TYPE_CHECKING
from enum import Enum

from .base import Base


if TYPE_CHECKING:
    from .orders import Order
    from .carts import Cart

class UserType(str, Enum):
    super_user = "super_user"
    admin = "admin"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user", cascade="all, delete")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete")
    type: Mapped[UserType] = mapped_column(SqlEnum(UserType), default=UserType.customer)
    password: Mapped[str] = mapped_column(nullable=True)
