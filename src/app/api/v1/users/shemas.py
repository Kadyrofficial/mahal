from pydantic import BaseModel, ConfigDict

from utils.mixins import PhoneMixin, CodeMixin, EmailMixin


class UserMeShema(BaseModel):
    phone: str
    email: str | None = None
    first_name: str
    last_name: str
    
    model_config = ConfigDict(from_attributes=True)


class UserMeUpdateNameShema(BaseModel):
    first_name: str
    last_name: str


class UserMeUpdatePhoneShema(PhoneMixin, BaseModel):
    pass


class UserMeVerifyPhoneShema(CodeMixin, UserMeUpdatePhoneShema):
    pass


class UserMeVerifyPhoneResponseSchema(BaseModel):
    token: str


class UserMeUpdateEmailShema(EmailMixin, BaseModel):
    pass


class UserMeVerifyEmailShema(CodeMixin, UserMeUpdateEmailShema):
    pass
