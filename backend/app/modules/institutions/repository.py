"""
Institution repository.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.institutions import queries as q


class InstitutionRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_by_id(self, institution_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_INSTITUTION_BY_ID, institution_id)
        return dict(row) if row else None

    async def get_summary(self, institution_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_INSTITUTION_SUMMARY, institution_id)
        return dict(row) if row else None

    async def list_all(self, limit: int, offset: int) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.LIST_INSTITUTIONS, limit, offset)
        return [dict(r) for r in rows]

    async def count_all(self) -> int:
        row = await self.conn.fetchrow(q.COUNT_INSTITUTIONS)
        return int(row["count"])  # type: ignore[index]

    async def update_status(
        self, institution_id: UUID, is_active: bool
    ) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(
            q.UPDATE_INSTITUTION_STATUS, institution_id, is_active
        )
        return dict(row) if row else None
