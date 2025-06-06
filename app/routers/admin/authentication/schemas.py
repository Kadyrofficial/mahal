from pydantic import BaseModel

from app.utils.mixins import PhoneMixin, PasswordMixin
from app.models import UserType


class LoginSchema(PhoneMixin, PasswordMixin, BaseModel):
    pass


class LoginResponseSchema(BaseModel):
    token: str
    type: UserType
