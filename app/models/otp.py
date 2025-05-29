from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum, DateTime
from enum import Enum
from datetime import datetime, timezone

from .base import Base


class Purpose(str, Enum):
    login = "login"
    change_phone = "change_phone",
    add_email = "add_email"


class OTP(Base):
    __tablename__ = "otps"

    phone_or_email: Mapped[str]
    code: Mapped[str]
    purpose: Mapped[Purpose] = mapped_column(SqlEnum(Purpose), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    use_count: Mapped[int] = mapped_column(default=0)
    is_used: Mapped[bool] = mapped_column(default=False)
