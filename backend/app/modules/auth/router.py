"""
Auth router — thin HTTP adapter, delegates to AuthService.
"""
from asyncpg import Connection
from fastapi import APIRouter, Depends, status

from app.core.database import get_connection
from app.core.dependencies import CurrentUserDep
from app.modules.auth.schemas import (
    LoginRequest,
    MFIRegistrationRequest,
    MFIRegistrationResponse,
    LearnerRegistrationRequest,
    RefreshRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService
from app.shared.responses import APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _svc(conn: Connection = Depends(get_connection)) -> AuthService:
    return AuthService(conn)


@router.post(
    "/register-mfi",
    response_model=APIResponse[MFIRegistrationResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new MFI and its first admin user",
)
async def register_mfi(
    payload: MFIRegistrationRequest,
    svc: AuthService = Depends(_svc),
) -> APIResponse[MFIRegistrationResponse]:
    result = await svc.register_mfi(payload)
    return APIResponse.created(result)


@router.post(
    "/register-learner",
    response_model=APIResponse[TokenResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new learner user and immediately log them in",
)
async def register_learner(
    payload: LearnerRegistrationRequest,
    svc: AuthService = Depends(_svc),
) -> APIResponse[TokenResponse]:
    tokens = await svc.register_learner(payload)
    return APIResponse.created(tokens, "Learner registered successfully")


@router.post(
    "/login",
    response_model=APIResponse[TokenResponse],
    summary="Authenticate with phone number and password",
)
async def login(
    payload: LoginRequest,
    svc: AuthService = Depends(_svc),
) -> APIResponse[TokenResponse]:
    tokens = await svc.login(payload)
    return APIResponse.ok(tokens, "Login successful")


@router.post(
    "/refresh",
    response_model=APIResponse[TokenResponse],
    summary="Rotate refresh token and issue new access token",
)
async def refresh(
    payload: RefreshRequest,
    svc: AuthService = Depends(_svc),
) -> APIResponse[TokenResponse]:
    tokens = await svc.refresh(payload.refresh_token)
    return APIResponse.ok(tokens, "Tokens refreshed")


@router.post(
    "/logout",
    response_model=APIResponse[None],
    summary="Revoke the current refresh token",
)
async def logout(
    payload: RefreshRequest,
    current_user: CurrentUserDep,
    svc: AuthService = Depends(_svc),
) -> APIResponse[None]:
    await svc.logout(payload.refresh_token)
    return APIResponse.no_content("Logged out successfully")
