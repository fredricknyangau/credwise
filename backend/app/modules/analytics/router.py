"""
Analytics router — MFI admin only.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, Query

from app.core.database import get_connection
from app.core.dependencies import MfiAdminDep
from app.core.exceptions import ForbiddenException
from app.modules.analytics.schemas import (
    HighRiskClient,
    InstitutionDashboard,
    LiteracyTrendPoint,
    ModuleCompletionRate,
)
from app.modules.analytics.service import AnalyticsService
from app.shared.responses import APIResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _svc(conn: Connection = Depends(get_connection)) -> AnalyticsService:
    return AnalyticsService(conn)


def _institution_id(admin: MfiAdminDep) -> UUID:
    """Extract institution_id from token — raises if missing."""
    if not admin.institution_id:
        raise ForbiddenException("No institution associated with this admin account")
    return admin.institution_id


@router.get(
    "/dashboard",
    response_model=APIResponse[InstitutionDashboard],
    summary="MFI dashboard summary — client counts, avg scores",
)
async def dashboard(
    admin: MfiAdminDep,
    svc: AnalyticsService = Depends(_svc),
) -> APIResponse[InstitutionDashboard]:
    inst_id = _institution_id(admin)
    data = await svc.get_dashboard(inst_id)
    return APIResponse.ok(data)


@router.get(
    "/high-risk",
    response_model=APIResponse[list[HighRiskClient]],
    summary="Clients with readiness score below 40",
)
async def high_risk(
    admin: MfiAdminDep,
    limit: int = Query(default=20, ge=1, le=100),
    svc: AnalyticsService = Depends(_svc),
) -> APIResponse[list[HighRiskClient]]:
    inst_id = _institution_id(admin)
    clients = await svc.get_high_risk_clients(inst_id, limit)
    return APIResponse.ok(clients)


@router.get(
    "/literacy-trend",
    response_model=APIResponse[list[LiteracyTrendPoint]],
    summary="Weekly lesson completion trend for last 12 weeks",
)
async def literacy_trend(
    admin: MfiAdminDep,
    svc: AnalyticsService = Depends(_svc),
) -> APIResponse[list[LiteracyTrendPoint]]:
    inst_id = _institution_id(admin)
    trend = await svc.get_literacy_trend(inst_id)
    return APIResponse.ok(trend)


@router.get(
    "/module-completion",
    response_model=APIResponse[list[ModuleCompletionRate]],
    summary="Completion rates per literacy module",
)
async def module_completion(
    admin: MfiAdminDep,
    svc: AnalyticsService = Depends(_svc),
) -> APIResponse[list[ModuleCompletionRate]]:
    inst_id = _institution_id(admin)
    rates = await svc.get_module_completion_rates(inst_id)
    return APIResponse.ok(rates)
