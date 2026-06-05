"""
Literacy service.
"""
from __future__ import annotations

import uuid
from uuid import UUID

from asyncpg import Connection

from app.core.exceptions import NotFoundException
from app.modules.literacy.repository import LiteracyRepository
from app.modules.literacy.schemas import (
    CreateLessonRequest,
    CreateModuleRequest,
    LessonRead,
    ModuleProgress,
    ModuleProgressSummary,
    ModuleRead,
)
from app.shared.pagination import PaginatedResponse, PaginationParams


class LiteracyService:
    def __init__(self, conn: Connection) -> None:
        self.repo = LiteracyRepository(conn)

    # ── Modules ───────────────────────────────────────────────────────────────

    async def create_module(self, payload: CreateModuleRequest) -> ModuleRead:
        row = await self.repo.insert_module(
            module_id=uuid.uuid4(),
            title=payload.title,
            description=payload.description,
            difficulty_level=payload.difficulty_level,
            estimated_minutes=payload.estimated_minutes,
        )
        return ModuleRead(**row)

    async def get_module(self, module_id: UUID) -> ModuleRead:
        row = await self.repo.get_module(module_id)
        if not row:
            raise NotFoundException("Module")
        return ModuleRead(**row)

    async def list_modules(
        self, params: PaginationParams
    ) -> PaginatedResponse[ModuleRead]:
        total = await self.repo.count_modules()
        rows = await self.repo.list_modules(params.limit, params.offset)
        items = [ModuleRead(**r) for r in rows]
        return PaginatedResponse.build(items, total, params)

    async def set_published(self, module_id: UUID, published: bool) -> ModuleRead:
        row = await self.repo.set_published(module_id, published)
        if not row:
            raise NotFoundException("Module")
        return await self.get_module(module_id)

    # ── Lessons ───────────────────────────────────────────────────────────────

    async def create_lesson(
        self, module_id: UUID, payload: CreateLessonRequest
    ) -> LessonRead:
        # Verify module exists
        await self.get_module(module_id)
        row = await self.repo.insert_lesson(
            lesson_id=uuid.uuid4(),
            module_id=module_id,
            title=payload.title,
            content=payload.content,
            lesson_order=payload.lesson_order,
        )
        return LessonRead(**row)

    async def get_lesson(self, lesson_id: UUID) -> LessonRead:
        row = await self.repo.get_lesson(lesson_id)
        if not row:
            raise NotFoundException("Lesson")
        return LessonRead(**row)

    async def list_lessons(self, module_id: UUID) -> list[LessonRead]:
        await self.get_module(module_id)
        rows = await self.repo.list_lessons(module_id)
        return [LessonRead(**r) for r in rows]

    # ── Progress ──────────────────────────────────────────────────────────────

    async def complete_lesson(self, user_id: UUID, lesson_id: UUID) -> dict:
        lesson = await self.repo.get_lesson(lesson_id)
        if not lesson:
            raise NotFoundException("Lesson")
        await self.repo.mark_lesson_complete(uuid.uuid4(), user_id, lesson_id)
        return {"message": "Lesson marked as complete"}

    async def get_module_progress(
        self, module_id: UUID, user_id: UUID
    ) -> ModuleProgress:
        row = await self.repo.get_module_progress(module_id, user_id)
        return ModuleProgress(**row)

    async def get_user_progress(
        self, user_id: UUID
    ) -> list[ModuleProgressSummary]:
        rows = await self.repo.get_all_progress(user_id)
        return [ModuleProgressSummary(**r) for r in rows]
