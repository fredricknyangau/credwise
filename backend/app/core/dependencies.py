"""
Shared FastAPI dependencies.

These are injected via Depends() throughout route handlers.
They never contain business logic — they resolve infrastructure concerns.
"""
from __future__ import annotations

from typing import Annotated
from uuid import UUID

from asyncpg import Connection
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import get_connection
from app.core.exceptions import ForbiddenException, InactiveAccountException
from app.core.security import decode_access_token

_bearer = HTTPBearer(auto_error=True)


# ---------------------------------------------------------------------------
# Token extraction
# ---------------------------------------------------------------------------

def _extract_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> dict:
    """Validate Bearer token and return its decoded payload."""
    return decode_access_token(credentials.credentials)


TokenPayload = Annotated[dict, Depends(_extract_token_payload)]
DBConn = Annotated[Connection, Depends(get_connection)]


# ---------------------------------------------------------------------------
# Current user identity
# ---------------------------------------------------------------------------

class CurrentUser:
    """Resolved from the JWT payload — no DB hit required."""

    def __init__(self, payload: TokenPayload) -> None:
        self.user_id: UUID = UUID(payload["sub"])
        self.role: str = payload["role"]
        self.institution_id: UUID | None = (
            UUID(payload["institution_id"])
            if payload.get("institution_id")
            else None
        )
        self.is_active: bool = payload.get("is_active", True)

    def require_active(self) -> "CurrentUser":
        if not self.is_active:
            raise InactiveAccountException()
        return self

    def require_role(self, *roles: str) -> "CurrentUser":
        if self.role not in roles:
            raise ForbiddenException(
                f"This action requires one of: {', '.join(roles)}"
            )
        return self


def get_current_user(payload: TokenPayload) -> CurrentUser:
    return CurrentUser(payload)


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


# ---------------------------------------------------------------------------
# Role-specific shortcut dependencies
# ---------------------------------------------------------------------------

def require_platform_admin(current_user: CurrentUserDep) -> CurrentUser:
    return current_user.require_role("platform_admin")


def require_mfi_admin(current_user: CurrentUserDep) -> CurrentUser:
    return current_user.require_role("mfi_admin", "platform_admin")


def require_client(current_user: CurrentUserDep) -> CurrentUser:
    return current_user.require_role("client", "mfi_admin", "platform_admin")


PlatformAdminDep = Annotated[CurrentUser, Depends(require_platform_admin)]
MfiAdminDep = Annotated[CurrentUser, Depends(require_mfi_admin)]
ClientDep = Annotated[CurrentUser, Depends(require_client)]
