from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from fastapi import Depends, Path
from typing import Annotated

from app.models import User, Cart
from app.utils import authentication
from app.db import db_helper


async def check_cart(
        cart_id: Annotated[int, Path(description="ID of the cart")],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        user: User = Depends(authentication.check_auth)) -> Cart:
    try:
        user_id = user.id
        result = await session.execute(
            select(Cart).options(selectinload(Cart.products)).where(
                Cart.user_id == user_id,
                Cart.id == cart_id
            )
        )
        cart = result.scalar_one()
        return cart
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cart not found")
