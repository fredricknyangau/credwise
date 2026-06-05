"""
Profile repository.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.profiles import queries as q


class ProfileRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def upsert(
        self,
        profile_id: UUID,
        user_id: UUID,
        monthly_income: float,
        savings_frequency: str,
        business_type: str,
        years_in_business: float,
        cooperative_member: bool,
        existing_loans: int,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.UPSERT_PROFILE,
            profile_id,
            user_id,
            monthly_income,
            savings_frequency,
            business_type,
            years_in_business,
            cooperative_member,
            existing_loans,
        )
        return dict(row)  # type: ignore[arg-type]

    async def get_by_user(self, user_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_PROFILE_BY_USER, user_id)
        return dict(row) if row else None
