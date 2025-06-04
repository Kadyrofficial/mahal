from pydantic import BaseModel

from app.utils.mixins import PhoneMixin


class LoginSchema(PhoneMixin):
    password: str


class TokenSchema(BaseModel):
    token: str
