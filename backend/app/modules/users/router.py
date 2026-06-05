"""
Users router.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, status

from app.core.database import get_connection
from app.core.dependencies import ClientDep, CurrentUserDep, MfiAdminDep
from app.core.exceptions import ForbiddenException
from app.modules.users.schemas import CreateClientRequest, UpdateUserStatusRequest, UserRead
from app.modules.users.service import UserService
from app.shared.pagination import PaginatedResponse, PaginationParams
from app.shared.responses import APIResponse

router = APIRouter(prefix="/users", tags=["Users"])


def _svc(conn: Connection = Depends(get_connection)) -> UserService:
    return UserService(conn)


@router.post(
    "/",
    response_model=APIResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    summary="MFI admin creates a client user",
)
async def create_client(
    payload: CreateClientRequest,
    current_user: MfiAdminDep,
    svc: UserService = Depends(_svc),
) -> APIResponse[UserRead]:
    if not current_user.institution_id:
        raise ForbiddenException("No institution associated with this account")
    user = await svc.create_client(payload, current_user.institution_id)
    return APIResponse.created(user)


@router.get(
    "/me",
    response_model=APIResponse[UserRead],
    summary="Get current user profile",
)
async def get_me(
    current_user: CurrentUserDep,
    svc: UserService = Depends(_svc),
) -> APIResponse[UserRead]:
    user = await svc.get_user(current_user.user_id)
    return APIResponse.ok(user)


@router.get(
    "/",
    response_model=APIResponse[PaginatedResponse[UserRead]],
    summary="List clients for the current MFI",
)
async def list_clients(
    current_user: MfiAdminDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    svc: UserService = Depends(_svc),
) -> APIResponse[PaginatedResponse[UserRead]]:
    if not current_user.institution_id:
        raise ForbiddenException("No institution associated with this account")
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.list_institution_clients(current_user.institution_id, params)
    return APIResponse.ok(result)


@router.get(
    "/{user_id}",
    response_model=APIResponse[UserRead],
    summary="Get a specific user by ID",
)
async def get_user(
    user_id: UUID,
    current_user: MfiAdminDep,
    svc: UserService = Depends(_svc),
) -> APIResponse[UserRead]:
    user = await svc.get_user(user_id)
    return APIResponse.ok(user)


@router.patch(
    "/{user_id}/status",
    response_model=APIResponse[UserRead],
    summary="Activate or deactivate a user",
)
async def update_status(
    user_id: UUID,
    payload: UpdateUserStatusRequest,
    current_user: MfiAdminDep,
    svc: UserService = Depends(_svc),
) -> APIResponse[UserRead]:
    user = await svc.update_status(user_id, payload.is_active)
    return APIResponse.ok(user)
