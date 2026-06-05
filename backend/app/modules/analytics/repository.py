"""
Analytics repository.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.analytics import queries as q


class AnalyticsRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_dashboard(self, institution_id: UUID) -> dict[str, Any]:
        row = await self.conn.fetchrow(q.INSTITUTION_DASHBOARD, institution_id)
        return dict(row) if row else {}

    async def get_high_risk_clients(
        self, institution_id: UUID, limit: int = 20
    ) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.HIGH_RISK_CLIENTS, institution_id, limit)
        return [dict(r) for r in rows]

    async def get_literacy_trend(
        self, institution_id: UUID
    ) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.LITERACY_TREND, institution_id)
        return [dict(r) for r in rows]

    async def get_module_completion_rates(
        self, institution_id: UUID
    ) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.MODULE_COMPLETION_RATES, institution_id)
        return [dict(r) for r in rows]
