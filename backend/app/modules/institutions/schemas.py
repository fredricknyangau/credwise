"""
Institution schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InstitutionRead(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    location: str
    is_active: bool
    created_at: datetime


class InstitutionSummary(BaseModel):
    id: UUID
    name: str
    email: str
    location: str
    is_active: bool
    created_at: datetime
    client_count: int
    admin_count: int


class UpdateInstitutionStatusRequest(BaseModel):
    is_active: bool
