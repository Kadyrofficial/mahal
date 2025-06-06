from pydantic import EmailStr, Field


class PhoneMixin:
    phone: str = Field(pattern=r"^\+993\d{8}$", description="Only phone numbers which start with +993")


class CodeMixin:
    code: int = Field(ge=1000, le=9999)


class EmailMixin:
    email: EmailStr


class PasswordMixin:
    password: str = Field(max_length=16, min_length=8)
