from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from db import db_helper
from models import User, Cart
from auth import auth_manager
from . import crud, utils
from .shemas import CartSchema, CartViewSchema, AddProductSchema, UpdateProductSchema, GetProductSchema
from . import dependencies


router = APIRouter(
    prefix="/carts",
    tags=["Carts🛍️"]
)


@router.get(
    path="/my_carts",
    name="Your Cart🛒",
    description="View your cart items in your cart",
    response_model=list[CartSchema]
)
async def get_my_cart(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(auth_manager.check_auth)
):
    return await crud.get_my_cart(session, user)


@router.get(
    path="/my_carts/{cart_id}",
    name="View Your Cart🛒👀",
    description="View your products in your cart",
    response_model=CartViewSchema
)
def view_cart(
    cart: Cart = Depends(dependencies.check_cart)
) -> CartViewSchema:
    return CartViewSchema.model_validate(cart)


@router.post(
    path="/my_carts/{cart_id}/order",
    name="Order Products🚚",
    description="Order products of your cart"
)
async def order(
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await utils.order(cart, session)


@router.post(
    path="/my_carts/{cart_id}/products",
    name="Add Product➕",
    description="Add products to your cart",
    response_model=AddProductSchema
)
async def add_product(
    product_in: AddProductSchema,
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.add_product(cart, product_in, session)


@router.get(
    path="/my_carts/{cart_id}/products/{product_id}",
    name="Get Product",
    description="Get product of your cart",
    response_model=GetProductSchema
)
def get_product(
    product_id: Annotated[int, Path(description="Id of the product")],
    cart: Cart = Depends(dependencies.check_cart),
) -> GetProductSchema:
    product_to_get = next((p for p in cart.products if p.id == product_id), None)
    return GetProductSchema.model_validate(product_to_get)


@router.put(
    path="/my_carts/{cart_id}/products/{product_id}",
    name="Update Product➕",
    description="Update product of your cart",
    response_model=UpdateProductSchema
)
async def update_product(
    product_in: UpdateProductSchema,
    product_id: Annotated[int, Path(description="Id of the product")],
    
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_product(product_in, product_id, cart, session)


@router.delete(
    path="/my_carts/{cart_id}/products/{product_id}",
    name="Delete Product❌",
    description="Depete product from your cart"
)
async def delete_product(
    product_id: Annotated[int, Path(description="Id of the product")],
    cart: Cart = Depends(dependencies.check_cart),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_product(cart, product_id, session)
