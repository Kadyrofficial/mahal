from pydantic import BaseModel

from utils.mixins import PhoneMixin, CodeMixin


class LoginSchema(PhoneMixin, BaseModel):
    pass


class VerifySchema(PhoneMixin, CodeMixin, BaseModel):
    pass


class VerifyResponseSchema(BaseModel):
    token: str
