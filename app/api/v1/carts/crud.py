from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User, Cart, Shipping, Product
from .shemas import CartSchema, AddProductSchema, UpdateProductSchema


async def get_my_cart(session: AsyncSession, user: User) -> list[CartSchema]:
    user_id = user.id
    result = await session.execute(
        select(Cart).where(
            Cart.user_id == user_id
        )
    )
    carts = result.scalars().all()
    if not carts:
        carts = []
        for shipping in Shipping:
            cart = Cart(
                user_id = user_id,
                shipping_method=shipping
            )
            carts.append(cart)
        session.add_all(carts)
        await session.commit()
    return [CartSchema.model_validate(cart) for cart in carts]


async def add_product(cart: Cart, product_in: AddProductSchema, session: AsyncSession, user: User) -> AddProductSchema:
    product = Product(
        **product_in.model_dump(),
        cart_id=cart.id
    )
    cart.product_count += 1
    session.add(product)
    await session.commit()
    return product_in


async def update_product(product_in: UpdateProductSchema, product_id: int, cart: Cart, session: AsyncSession) -> UpdateProductSchema:
    product_to_update = next((p for p in cart.products if p.id == product_id), None)
    if not product_to_update:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    for key, value in product_in.model_dump().items():
        setattr(product_to_update, key, value)
    await session.commit()
    return product_in


async def delete_product(cart: Cart, product_id: int, session: AsyncSession):
    product_to_delete = next((p for p in cart.products if p.id == product_id), None)
    if not product_to_delete:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    cart.product_count -= 1
    await session.delete(product_to_delete)
    await session.commit()
    return Response(status_code=204)
