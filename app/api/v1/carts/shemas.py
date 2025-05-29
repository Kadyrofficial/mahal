from pydantic import BaseModel, ConfigDict
from typing import List

from models import Shipping


class AddProductSchema(BaseModel):
    name: str
    description: str | None = None
    link: str | None = None
    quantity: int | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateProductSchema(AddProductSchema):
    pass


class GetProductSchema(AddProductSchema):
    pass


class ListProductSchema(BaseModel):
    id: int
    name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class CartSchema(BaseModel):
    id: int
    product_count: int
    shipping_method: Shipping
    
    model_config = ConfigDict(from_attributes=True)


class CartViewSchema(CartSchema):
    products: List[ListProductSchema]

    model_config = ConfigDict(from_attributes=True)
    