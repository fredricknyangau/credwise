"""
Analytics service.
"""
from __future__ import annotations

from uuid import UUID

from asyncpg import Connection

from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.schemas import (
    HighRiskClient,
    InstitutionDashboard,
    LiteracyTrendPoint,
    ModuleCompletionRate,
)


class AnalyticsService:
    def __init__(self, conn: Connection) -> None:
        self.repo = AnalyticsRepository(conn)

    async def get_dashboard(self, institution_id: UUID) -> InstitutionDashboard:
        row = await self.repo.get_dashboard(institution_id)
        return InstitutionDashboard(**row)

    async def get_high_risk_clients(
        self, institution_id: UUID, limit: int = 20
    ) -> list[HighRiskClient]:
        rows = await self.repo.get_high_risk_clients(institution_id, limit)
        return [HighRiskClient(**r) for r in rows]

    async def get_literacy_trend(
        self, institution_id: UUID
    ) -> list[LiteracyTrendPoint]:
        rows = await self.repo.get_literacy_trend(institution_id)
        return [LiteracyTrendPoint(**r) for r in rows]

    async def get_module_completion_rates(
        self, institution_id: UUID
    ) -> list[ModuleCompletionRate]:
        rows = await self.repo.get_module_completion_rates(institution_id)
        return [ModuleCompletionRate(**r) for r in rows]
