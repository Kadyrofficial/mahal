from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db import db_helper
from app.models import User, Cart
from app.utils import authentication
from . import crud, utils
from .shemas import CartSchema, CartViewSchema, ProductSchema
from . import dependencies


router = APIRouter(
    prefix="/carts",
    tags=["Carts🛍️"]
)


@router.get(
    path="/my_carts",
    summary="Get your carts",
    response_model=list[CartSchema]
)
async def get_my_cart(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(authentication.check_auth)
):
    return await crud.get_my_cart(session, user)


@router.get(
    path="/my_carts/{cart_id}",
    summary="Get your cart",
    response_model=CartViewSchema
)
def view_cart(
    cart: Cart = Depends(dependencies.check_cart)
) -> CartViewSchema:
    return CartViewSchema.model_validate(cart)


@router.post(
    path="/my_carts/{cart_id}/order",
    summary="Order products in your cart",
    response_model=CartViewSchema
)
async def order(
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await utils.order(cart, session)


@router.post(
    path="/my_carts/{cart_id}/products",
    summary="Add product",
    response_model=ProductSchema
)
async def add_product(
    product_in: ProductSchema,
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.add_product(cart, product_in, session)


@router.get(
    path="/my_carts/{cart_id}/products/{product_id}",
    summary="Get product",
    response_model=ProductSchema
)
def get_product(
    product_id: Annotated[int, Path(description="Id of the product")],
    cart: Cart = Depends(dependencies.check_cart),
) -> ProductSchema:
    product_to_get = next((p for p in cart.products if p.id == product_id), None)
    return ProductSchema.model_validate(product_to_get)


@router.put(
    path="/my_carts/{cart_id}/products/{product_id}",
    summary="Update product",
    response_model=ProductSchema
)
async def update_product(
    product_in: ProductSchema,
    product_id: Annotated[int, Path(description="Id of the product")],
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_product(product_in, product_id, cart, session)


@router.delete(
    path="/my_carts/{cart_id}/products/{product_id}",
    summary="Delete product",
)
async def delete_product(
    product_id: Annotated[int, Path(description="Product id")],
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_product(cart, product_id, session)
