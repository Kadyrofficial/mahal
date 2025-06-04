from pydantic import BaseModel, ConfigDict, Field
from typing import List

from app.models import Shipping


class ListProductSchema(BaseModel):
    id: int
    name: str = Field(max_length=150)
    quantity: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(ListProductSchema):
    description: str | None = None
    link: str | None = None


class CartSchema(BaseModel):
    id: int
    product_count: int
    shipping_method: Shipping

    model_config = ConfigDict(from_attributes=True)


class CartViewSchema(CartSchema):
    products: List[ListProductSchema]
