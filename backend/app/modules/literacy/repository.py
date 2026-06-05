"""
Literacy repository.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.literacy import queries as q


class LiteracyRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    # ── Modules ───────────────────────────────────────────────────────────────

    async def list_modules(self, limit: int, offset: int) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.LIST_MODULES, limit, offset)
        return [dict(r) for r in rows]

    async def count_modules(self) -> int:
        row = await self.conn.fetchrow(q.COUNT_MODULES)
        return int(row["count"])  # type: ignore[index]

    async def get_module(self, module_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_MODULE_BY_ID, module_id)
        return dict(row) if row else None

    async def insert_module(
        self,
        module_id: UUID,
        title: str,
        description: str,
        difficulty_level: str,
        estimated_minutes: int,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_MODULE,
            module_id, title, description, difficulty_level, estimated_minutes,
        )
        return dict(row)  # type: ignore[arg-type]

    async def set_published(self, module_id: UUID, published: bool) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.PUBLISH_MODULE, module_id, published)
        return dict(row) if row else None

    # ── Lessons ───────────────────────────────────────────────────────────────

    async def list_lessons(self, module_id: UUID) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.LIST_LESSONS_BY_MODULE, module_id)
        return [dict(r) for r in rows]

    async def get_lesson(self, lesson_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_LESSON_BY_ID, lesson_id)
        return dict(row) if row else None

    async def insert_lesson(
        self,
        lesson_id: UUID,
        module_id: UUID,
        title: str,
        content: str,
        lesson_order: int,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_LESSON,
            lesson_id, module_id, title, content, lesson_order,
        )
        return dict(row)  # type: ignore[arg-type]

    # ── Progress ──────────────────────────────────────────────────────────────

    async def mark_lesson_complete(
        self, completion_id: UUID, user_id: UUID, lesson_id: UUID
    ) -> bool:
        row = await self.conn.fetchrow(
            q.UPSERT_LESSON_COMPLETION, completion_id, user_id, lesson_id
        )
        return row is not None

    async def get_module_progress(
        self, module_id: UUID, user_id: UUID
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(q.GET_MODULE_PROGRESS, module_id, user_id)
        return dict(row)  # type: ignore[arg-type]

    async def get_all_progress(self, user_id: UUID) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.GET_ALL_MODULES_PROGRESS, user_id)
        return [dict(r) for r in rows]
