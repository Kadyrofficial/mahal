from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils import password_manager
from app.models import User, UserType
from app.core import settings


phone: str = input("Phone Number: ")

if not [phone.startswith("+993") and len(phone) == 12, phone.strip("+").isdigit()]:
    raise ValueError("Invalid phone number")

password: str = input("Password: ")

if len(password) < 8 or (len(password) > 16):
    raise ValueError("Password must be at least 8 characters long and less than 16 characters long")

def create_superuser(phone: str = phone, password: str = password):
    engine = create_engine(url=settings.sync_db_url)

    with Session(engine) as session:
        result = session.execute(
            select(User).where(
                User.phone == phone,
            )
        )

        user = result.scalar_one_or_none()

        if user:
            raise ValueError(f"User with phone number {phone} already exists")

        user = User(
            phone=phone,
            password=password_manager.hash_password(password),
            type=UserType.super_user,
            is_active=True,
        )


        session.add(user)

        session.commit()

    print(f"Created superuser with phone number {phone}")

create_superuser(phone, password)
