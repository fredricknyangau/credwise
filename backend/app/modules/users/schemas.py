"""
User schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.shared.validators import validate_password_strength, validate_phone


class CreateClientRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=200)
    phone_number: str
    password: str

    @field_validator("phone_number")
    @classmethod
    def phone_format(cls, v: str) -> str:
        return validate_phone(v)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return validate_password_strength(v)


class UserRead(BaseModel):
    id: UUID
    institution_id: UUID | None
    role: str
    full_name: str
    phone_number: str
    is_active: bool
    created_at: datetime


class UpdateUserStatusRequest(BaseModel):
    is_active: bool
