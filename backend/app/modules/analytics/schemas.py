"""
Analytics schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InstitutionDashboard(BaseModel):
    total_clients: int
    active_clients: int
    avg_literacy_completion: float
    avg_readiness_score: float


class HighRiskClient(BaseModel):
    id: UUID
    full_name: str
    phone_number: str
    score: float
    rating: str
    scored_at: datetime


class LiteracyTrendPoint(BaseModel):
    week: datetime
    completions: int


class ModuleCompletionRate(BaseModel):
    module_id: UUID
    title: str
    enrolled_clients: int
    completed_clients: int
    completion_rate: float
