from pydantic import EmailStr, Field, BaseModel


class PhoneMixin(BaseModel):
    phone: str = Field(pattern=r"^\+993\d{8}$", description="Only phone numbers which start with +993")


class CodeMixin(BaseModel):
    code: int = Field(ge=1000, le=9999)


class EmailMixin(BaseModel):
    email: EmailStr
