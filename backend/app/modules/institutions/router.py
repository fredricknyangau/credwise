"""
Institutions router — platform admin only.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, status

from app.core.database import get_connection
from app.core.dependencies import MfiAdminDep, PlatformAdminDep
from app.modules.institutions.schemas import (
    InstitutionRead,
    InstitutionSummary,
    UpdateInstitutionStatusRequest,
)
from app.modules.institutions.service import InstitutionService
from app.shared.pagination import PaginatedResponse, PaginationParams
from app.shared.responses import APIResponse

router = APIRouter(prefix="/institutions", tags=["Institutions"])


def _svc(conn: Connection = Depends(get_connection)) -> InstitutionService:
    return InstitutionService(conn)


@router.get(
    "/",
    response_model=APIResponse[PaginatedResponse[InstitutionRead]],
    summary="Platform admin: list all MFIs",
)
async def list_institutions(
    _admin: PlatformAdminDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    svc: InstitutionService = Depends(_svc),
) -> APIResponse[PaginatedResponse[InstitutionRead]]:
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.list_institutions(params)
    return APIResponse.ok(result)


@router.get(
    "/{institution_id}",
    response_model=APIResponse[InstitutionRead],
    summary="Get institution by ID",
)
async def get_institution(
    institution_id: UUID,
    _admin: MfiAdminDep,
    svc: InstitutionService = Depends(_svc),
) -> APIResponse[InstitutionRead]:
    institution = await svc.get_institution(institution_id)
    return APIResponse.ok(institution)


@router.get(
    "/{institution_id}/summary",
    response_model=APIResponse[InstitutionSummary],
    summary="Get institution summary with client/admin counts",
)
async def get_summary(
    institution_id: UUID,
    _admin: MfiAdminDep,
    svc: InstitutionService = Depends(_svc),
) -> APIResponse[InstitutionSummary]:
    summary = await svc.get_summary(institution_id)
    return APIResponse.ok(summary)


@router.patch(
    "/{institution_id}/status",
    response_model=APIResponse[InstitutionRead],
    summary="Platform admin: activate or suspend an MFI",
)
async def update_status(
    institution_id: UUID,
    payload: UpdateInstitutionStatusRequest,
    _admin: PlatformAdminDep,
    svc: InstitutionService = Depends(_svc),
) -> APIResponse[InstitutionRead]:
    result = await svc.update_status(institution_id, payload.is_active)
    return APIResponse.ok(result)
