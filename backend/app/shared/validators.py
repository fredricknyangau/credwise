"""
Shared custom validators used across schemas.
"""
import re


PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def validate_phone(v: str) -> str:
    v = v.strip().replace(" ", "").replace("-", "")
    if not PHONE_RE.match(v):
        raise ValueError("Invalid phone number format")
    return v


def validate_email(v: str) -> str:
    v = v.strip().lower()
    if not EMAIL_RE.match(v):
        raise ValueError("Invalid email format")
    return v


def validate_password_strength(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least one digit")
    return v
