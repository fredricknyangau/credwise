"""
JWT token generation / validation and bcrypt password hashing.

Design decisions:
- Access tokens are short-lived (configurable, default 30 min).
- Refresh tokens are long-lived (default 7 days), stored hashed in DB.
- python-jose is used for JWT; passlib[bcrypt] for password hashing.
- Role is embedded in the access token to avoid extra DB round-trips on every request.
"""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.core.exceptions import CredentialsException, TokenExpiredException

settings = get_settings()

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# Refresh token helpers
# ---------------------------------------------------------------------------

def generate_refresh_token() -> tuple[str, str]:
    """
    Returns (raw_token, hashed_token).
    Only the hash is persisted; the raw token is given to the client.
    """
    raw = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed


def hash_refresh_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


# ---------------------------------------------------------------------------
# JWT access tokens
# ---------------------------------------------------------------------------

def create_access_token(
    subject: str | UUID,
    role: str,
    institution_id: str | UUID | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: user UUID (stored as str in 'sub' claim)
        role: user role string ('platform_admin', 'mfi_admin', 'client')
        institution_id: optional MFI UUID for scoped authorization
        extra_claims: any additional claims to embed
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    if institution_id is not None:
        payload["institution_id"] = str(institution_id)
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Raises:
        TokenExpiredException: token has passed its 'exp' claim
        CredentialsException: token is malformed or signature invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("type") != "access":
            raise CredentialsException("Invalid token type")
        return payload
    except JWTError as exc:
        if "expired" in str(exc).lower():
            raise TokenExpiredException() from exc
        raise CredentialsException("Could not validate credentials") from exc


def create_refresh_token_expiry() -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
