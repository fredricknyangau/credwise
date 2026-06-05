"""
Literacy router.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, status

from app.core.database import get_connection
from app.core.dependencies import ClientDep, MfiAdminDep
from app.modules.literacy.schemas import (
    CompleteLesson,
    CreateLessonRequest,
    CreateModuleRequest,
    LessonRead,
    ModuleProgress,
    ModuleProgressSummary,
    ModuleRead,
)
from app.modules.literacy.service import LiteracyService
from app.shared.pagination import PaginatedResponse, PaginationParams
from app.shared.responses import APIResponse

router = APIRouter(prefix="/literacy", tags=["Financial Literacy"])


def _svc(conn: Connection = Depends(get_connection)) -> LiteracyService:
    return LiteracyService(conn)


# ── Modules ───────────────────────────────────────────────────────────────────

@router.get(
    "/modules",
    response_model=APIResponse[PaginatedResponse[ModuleRead]],
    summary="List all published literacy modules",
)
async def list_modules(
    _user: ClientDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[PaginatedResponse[ModuleRead]]:
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.list_modules(params)
    return APIResponse.ok(result)


@router.get(
    "/modules/{module_id}",
    response_model=APIResponse[ModuleRead],
    summary="Get module details",
)
async def get_module(
    module_id: UUID,
    _user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[ModuleRead]:
    module = await svc.get_module(module_id)
    return APIResponse.ok(module)


@router.post(
    "/modules",
    response_model=APIResponse[ModuleRead],
    status_code=status.HTTP_201_CREATED,
    summary="MFI admin: create a literacy module",
)
async def create_module(
    payload: CreateModuleRequest,
    _admin: MfiAdminDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[ModuleRead]:
    module = await svc.create_module(payload)
    return APIResponse.created(module)


@router.patch(
    "/modules/{module_id}/publish",
    response_model=APIResponse[ModuleRead],
    summary="MFI admin: publish or unpublish a module",
)
async def publish_module(
    module_id: UUID,
    published: bool = Query(...),
    _admin: MfiAdminDep = None,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[ModuleRead]:
    module = await svc.set_published(module_id, published)
    return APIResponse.ok(module)


# ── Lessons ───────────────────────────────────────────────────────────────────

@router.get(
    "/modules/{module_id}/lessons",
    response_model=APIResponse[list[LessonRead]],
    summary="List lessons in a module",
)
async def list_lessons(
    module_id: UUID,
    _user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[list[LessonRead]]:
    lessons = await svc.list_lessons(module_id)
    return APIResponse.ok(lessons)


@router.get(
    "/lessons/{lesson_id}",
    response_model=APIResponse[LessonRead],
    summary="Read a single lesson",
)
async def get_lesson(
    lesson_id: UUID,
    _user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[LessonRead]:
    lesson = await svc.get_lesson(lesson_id)
    return APIResponse.ok(lesson)


@router.post(
    "/modules/{module_id}/lessons",
    response_model=APIResponse[LessonRead],
    status_code=status.HTTP_201_CREATED,
    summary="MFI admin: add a lesson to a module",
)
async def create_lesson(
    module_id: UUID,
    payload: CreateLessonRequest,
    _admin: MfiAdminDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[LessonRead]:
    lesson = await svc.create_lesson(module_id, payload)
    return APIResponse.created(lesson)


# ── Progress ──────────────────────────────────────────────────────────────────

@router.post(
    "/lessons/complete",
    response_model=APIResponse[dict],
    summary="Mark a lesson as complete",
)
async def complete_lesson(
    payload: CompleteLesson,
    current_user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[dict]:
    result = await svc.complete_lesson(current_user.user_id, payload.lesson_id)
    return APIResponse.ok(result)


@router.get(
    "/modules/{module_id}/progress",
    response_model=APIResponse[ModuleProgress],
    summary="Get progress for a specific module",
)
async def get_module_progress(
    module_id: UUID,
    current_user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[ModuleProgress]:
    progress = await svc.get_module_progress(module_id, current_user.user_id)
    return APIResponse.ok(progress)


@router.get(
    "/progress",
    response_model=APIResponse[list[ModuleProgressSummary]],
    summary="Get progress across all modules for the current user",
)
async def get_user_progress(
    current_user: ClientDep,
    svc: LiteracyService = Depends(_svc),
) -> APIResponse[list[ModuleProgressSummary]]:
    progress = await svc.get_user_progress(current_user.user_id)
    return APIResponse.ok(progress)
