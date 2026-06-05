"""
Auth repository — executes raw SQL, maps results to dicts.
No business logic here. No ORM.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.auth import queries as q


class AuthRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    # ── Institutions ─────────────────────────────────────────────────────────

    async def institution_email_exists(self, email: str) -> bool:
        row = await self.conn.fetchrow(q.FIND_INSTITUTION_BY_EMAIL, email)
        return row is not None

    async def phone_exists(self, phone: str) -> bool:
        row = await self.conn.fetchrow(q.FIND_USER_BY_PHONE_EXISTS, phone)
        return row is not None

    async def insert_institution(
        self,
        id: UUID,
        name: str,
        email: str,
        phone: str,
        location: str,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_INSTITUTION, id, name, email, phone, location
        )
        return dict(row)  # type: ignore[arg-type]

    async def insert_mfi_admin(
        self,
        id: UUID,
        institution_id: UUID,
        full_name: str,
        phone_number: str,
        password_hash: str,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_MFI_ADMIN_USER,
            id,
            institution_id,
            full_name,
            phone_number,
            password_hash,
        )
        return dict(row)  # type: ignore[arg-type]

    async def insert_learner_user(
        self,
        id: UUID,
        full_name: str,
        phone_number: str,
        password_hash: str,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_LEARNER_USER,
            id,
            full_name,
            phone_number,
            password_hash,
        )
        return dict(row)  # type: ignore[arg-type]

    # ── Users ─────────────────────────────────────────────────────────────────

    async def find_user_by_phone(self, phone: str) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.FIND_USER_BY_PHONE, phone)
        return dict(row) if row else None

    async def find_user_by_id(self, user_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.FIND_USER_BY_ID, user_id)
        return dict(row) if row else None

    # ── Refresh Tokens ────────────────────────────────────────────────────────

    async def insert_refresh_token(
        self,
        token_id: UUID,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> None:
        await self.conn.execute(
            q.INSERT_REFRESH_TOKEN, token_id, user_id, token_hash, expires_at
        )

    async def find_refresh_token(self, token_hash: str) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.FIND_REFRESH_TOKEN, token_hash)
        return dict(row) if row else None

    async def revoke_refresh_token(self, token_hash: str) -> None:
        await self.conn.execute(q.REVOKE_REFRESH_TOKEN, token_hash)

    async def revoke_all_user_tokens(self, user_id: UUID) -> None:
        await self.conn.execute(q.REVOKE_ALL_USER_TOKENS, user_id)
