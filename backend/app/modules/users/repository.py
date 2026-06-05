"""
User repository.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.users import queries as q


class UserRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_by_id(self, user_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_USER_BY_ID, user_id)
        return dict(row) if row else None

    async def list_by_institution(
        self, institution_id: UUID, limit: int, offset: int
    ) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(
            q.LIST_USERS_BY_INSTITUTION, institution_id, limit, offset
        )
        return [dict(r) for r in rows]

    async def count_by_institution(self, institution_id: UUID) -> int:
        row = await self.conn.fetchrow(q.COUNT_USERS_BY_INSTITUTION, institution_id)
        return int(row["count"])  # type: ignore[index]

    async def insert_client(
        self,
        user_id: UUID,
        institution_id: UUID,
        full_name: str,
        phone_number: str,
        password_hash: str,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_CLIENT_USER,
            user_id,
            institution_id,
            full_name,
            phone_number,
            password_hash,
        )
        return dict(row)  # type: ignore[arg-type]

    async def phone_exists(self, phone: str, exclude_id: UUID | None = None) -> bool:
        exclude = exclude_id or UUID("00000000-0000-0000-0000-000000000000")
        row = await self.conn.fetchrow(q.CHECK_PHONE_EXISTS, phone, exclude)
        return row is not None

    async def update_status(
        self, user_id: UUID, is_active: bool
    ) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.UPDATE_USER_STATUS, user_id, is_active)
        return dict(row) if row else None
