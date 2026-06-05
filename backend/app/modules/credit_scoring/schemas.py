"""
Credit scoring schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreditScoreRead(BaseModel):
    id: UUID
    user_id: UUID
    score: float
    rating: str
    literacy_weight: float
    savings_weight: float
    stability_weight: float
    repayment_weight: float
    cooperative_weight: float
    factors: list[str]
    generated_at: datetime


class CreditScoreSummary(BaseModel):
    score: float
    rating: str
    factors: list[str]
    generated_at: datetime
