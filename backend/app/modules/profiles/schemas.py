"""
Profile schemas.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


SavingsFrequency = Literal["daily", "weekly", "bi_weekly", "monthly", "irregular"]
BusinessType = Literal[
    "farming", "trading", "services", "manufacturing", "none", "other"
]


class UpsertProfileRequest(BaseModel):
    monthly_income: float = Field(..., ge=0, description="Monthly income in KES")
    savings_frequency: SavingsFrequency
    business_type: BusinessType
    years_in_business: float = Field(..., ge=0)
    cooperative_member: bool
    existing_loans: int = Field(..., ge=0, description="Number of active loans")


class ProfileRead(BaseModel):
    id: UUID
    user_id: UUID
    monthly_income: float
    savings_frequency: str
    business_type: str
    years_in_business: float
    cooperative_member: bool
    existing_loans: int
    updated_at: datetime
