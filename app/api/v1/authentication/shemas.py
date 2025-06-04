from pydantic import BaseModel

from app.utils.mixins import PhoneMixin, CodeMixin


class LoginSchema(PhoneMixin, BaseModel):
    pass


class VerifySchema(PhoneMixin, CodeMixin, BaseModel):
    pass


class TokenSchema(BaseModel):
    token: str
