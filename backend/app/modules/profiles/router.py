"""
Profiles router.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, status

from app.core.database import get_connection
from app.core.dependencies import ClientDep, MfiAdminDep
from app.modules.profiles.schemas import ProfileRead, UpsertProfileRequest
from app.modules.profiles.service import ProfileService
from app.shared.responses import APIResponse

router = APIRouter(prefix="/profiles", tags=["Financial Profiles"])


def _svc(conn: Connection = Depends(get_connection)) -> ProfileService:
    return ProfileService(conn)


@router.put(
    "/me",
    response_model=APIResponse[ProfileRead],
    summary="Create or update own financial profile",
)
async def upsert_my_profile(
    payload: UpsertProfileRequest,
    current_user: ClientDep,
    svc: ProfileService = Depends(_svc),
) -> APIResponse[ProfileRead]:
    profile = await svc.upsert_profile(current_user.user_id, payload)
    return APIResponse.ok(profile, "Profile saved")


@router.get(
    "/me",
    response_model=APIResponse[ProfileRead],
    summary="Get own financial profile",
)
async def get_my_profile(
    current_user: ClientDep,
    svc: ProfileService = Depends(_svc),
) -> APIResponse[ProfileRead]:
    profile = await svc.get_profile(current_user.user_id)
    return APIResponse.ok(profile)


@router.get(
    "/{user_id}",
    response_model=APIResponse[ProfileRead],
    summary="MFI admin: view a client's financial profile",
)
async def get_client_profile(
    user_id: UUID,
    _admin: MfiAdminDep,
    svc: ProfileService = Depends(_svc),
) -> APIResponse[ProfileRead]:
    profile = await svc.get_profile(user_id)
    return APIResponse.ok(profile)
