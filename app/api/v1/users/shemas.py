from pydantic import BaseModel, ConfigDict

from app.utils.mixins import PhoneMixin, CodeMixin, EmailMixin


class NameShema(BaseModel):
    first_name: str
    last_name: str


class MeShema(NameShema):
    phone: str
    email: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class PhoneShema(PhoneMixin):
    pass


class VerifyPhoneShema(CodeMixin, PhoneMixin):
    pass


class EmailShema(EmailMixin):
    pass


class VerifyEmailShema(CodeMixin, EmailMixin):
    pass
