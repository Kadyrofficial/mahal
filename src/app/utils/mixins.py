from pydantic import field_validator
import re


class PhoneMixin:
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.startswith("+993"):
            raise ValueError("Phone number must start with +993")
        if not v[1:].isdigit():
            raise ValueError("Phone number must contain digits after +993")
        if len(v) != 12:
            raise ValueError("Phone number must be 12 characters long")
        return v
    

class CodeMixin:
    code: str
    
    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("OTP must contain only digits")
        if len(v) != 4:
            raise ValueError("OTP must be 4 characters long")
        return v


EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class EmailMixin:
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format: must contain '@' and '.' in the correct positions")
        return v
