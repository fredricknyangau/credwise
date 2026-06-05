"""
Auth module Pydantic schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.shared.validators import validate_password_strength, validate_phone


# ─── MFI Registration ────────────────────────────────────────────────────────

class MFIRegistrationRequest(BaseModel):
    # Institution fields
    institution_name: str = Field(..., min_length=2, max_length=200)
    institution_email: EmailStr
    institution_phone: str
    institution_location: str = Field(..., min_length=2, max_length=300)

    # Admin user fields
    admin_full_name: str = Field(..., min_length=2, max_length=200)
    admin_phone: str
    admin_password: str

    @field_validator("institution_phone", "admin_phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        return validate_phone(v)

    @field_validator("admin_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return validate_password_strength(v)


class MFIRegistrationResponse(BaseModel):
    institution_id: UUID
    institution_name: str
    admin_id: UUID
    admin_full_name: str
    role: str


# ─── Login ────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    phone_number: str
    password: str

    @field_validator("phone_number")
    @classmethod
    def phone_format(cls, v: str) -> str:
        return validate_phone(v)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshRequest(BaseModel):
    refresh_token: str


# ─── User info (returned inside token response) ───────────────────────────────

class UserInfo(BaseModel):
    id: UUID
    full_name: str
    role: str
    institution_id: UUID | None
    is_active: bool
