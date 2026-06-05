"""
Centralised exception hierarchy for Credwise.

Each domain exception maps to a specific HTTP status code, keeping
route handlers thin — they never construct HTTPException directly.
"""
from fastapi import HTTPException, status


class CredwiseBaseException(Exception):
    """Base for all application-level exceptions."""


# ---------------------------------------------------------------------------
# Auth exceptions
# ---------------------------------------------------------------------------

class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Insufficient permissions") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class InactiveAccountException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Contact your MFI administrator.",
        )


# ---------------------------------------------------------------------------
# Resource exceptions
# ---------------------------------------------------------------------------

class NotFoundException(HTTPException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class AlreadyExistsException(HTTPException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
        )


class ValidationException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


# ---------------------------------------------------------------------------
# Database exceptions
# ---------------------------------------------------------------------------

class DatabaseException(CredwiseBaseException):
    """Wraps low-level asyncpg errors for the service layer."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
