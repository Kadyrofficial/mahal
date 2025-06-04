from pydantic import BaseModel, ConfigDict
from typing import List


class UserSchema(BaseModel):
    id: int
    phone: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ListUserSchema(BaseModel):
    total: int
    pages: int
    limit: int
    users: List[UserSchema]
