from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response
from fastapi import HTTPException

from models import Order, Cart


async def order(cart: Cart, session: AsyncSession):
    if not cart.products:
        raise HTTPException(status_code=404, detail="Product not found")
    new_order = Order(
        user_id=cart.user.id,
        product_count=cart.product_count,
        shipping_method=cart.shipping_method,
        products=cart.products,
        status="active"
    )
    session.add(new_order)
    cart.products.clear()
    cart.product_count = 0
    await session.commit()
    return Response(status_code=200, content="Order created successfully")
