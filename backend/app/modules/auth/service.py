"""
Auth service — business logic layer.

Coordinates between AuthRepository, security utilities, and schemas.
All database mutations are wrapped in explicit transactions.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from asyncpg import Connection

from app.core.database import transaction
from app.core.exceptions import (
    AlreadyExistsException,
    BadRequestException,
    CredentialsException,
    InactiveAccountException,
    NotFoundException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token_expiry,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.core.config import get_settings
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    LoginRequest,
    MFIRegistrationRequest,
    MFIRegistrationResponse,
    TokenResponse,
)

settings = get_settings()


class AuthService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.repo = AuthRepository(conn)

    async def register_mfi(
        self, payload: MFIRegistrationRequest
    ) -> MFIRegistrationResponse:
        """
        Atomically creates an MFI institution + its first admin user.

        Checks uniqueness of institution email and admin phone before insert.
        Rolls back both inserts if either fails.
        """
        if await self.repo.institution_email_exists(payload.institution_email):
            raise AlreadyExistsException("Institution with this email")

        if await self.repo.phone_exists(payload.admin_phone):
            raise AlreadyExistsException("User with this phone number")

        institution_id = uuid.uuid4()
        admin_id = uuid.uuid4()
        password_hash = hash_password(payload.admin_password)

        async with transaction(self.conn):
            institution = await self.repo.insert_institution(
                id=institution_id,
                name=payload.institution_name,
                email=str(payload.institution_email),
                phone=payload.institution_phone,
                location=payload.institution_location,
            )
            admin = await self.repo.insert_mfi_admin(
                id=admin_id,
                institution_id=institution_id,
                full_name=payload.admin_full_name,
                phone_number=payload.admin_phone,
                password_hash=password_hash,
            )

        return MFIRegistrationResponse(
            institution_id=institution["id"],
            institution_name=institution["name"],
            admin_id=admin["id"],
            admin_full_name=admin["full_name"],
            role=admin["role"],
        )

    async def login(self, payload: LoginRequest) -> TokenResponse:
        """
        Authenticates a user by phone + password.

        On success, issues a short-lived access token + long-lived refresh token.
        The refresh token is stored hashed in the database.
        """
        user = await self.repo.find_user_by_phone(payload.phone_number)
        if not user:
            # Return same error for unknown phone to avoid user enumeration
            raise CredentialsException("Invalid credentials")

        if not verify_password(payload.password, user["password_hash"]):
            raise CredentialsException("Invalid credentials")

        if not user["is_active"]:
            raise InactiveAccountException()

        # Issue tokens
        access_token = create_access_token(
            subject=user["id"],
            role=user["role"],
            institution_id=user.get("institution_id"),
        )
        raw_refresh, hashed_refresh = generate_refresh_token()
        expires_at = create_refresh_token_expiry()

        await self.repo.insert_refresh_token(
            token_id=uuid.uuid4(),
            user_id=user["id"],
            token_hash=hashed_refresh,
            expires_at=expires_at,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=raw_refresh,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def refresh(self, raw_token: str) -> TokenResponse:
        """
        Validates a refresh token and issues a new token pair (rotation).

        The old refresh token is revoked before the new one is issued.
        """
        token_hash = hash_refresh_token(raw_token)
        record = await self.repo.find_refresh_token(token_hash)

        if not record:
            raise CredentialsException("Invalid refresh token")

        if record["revoked"]:
            # Token reuse — potential theft. Revoke all tokens for this user.
            await self.repo.revoke_all_user_tokens(record["user_id"])
            raise CredentialsException("Refresh token has been revoked")

        if record["expires_at"].replace(tzinfo=timezone.utc) < datetime.now(
            tz=timezone.utc
        ):
            raise CredentialsException("Refresh token has expired")

        user = await self.repo.find_user_by_id(record["user_id"])
        if not user or not user["is_active"]:
            raise InactiveAccountException()

        # Rotate: revoke old, issue new pair
        async with transaction(self.conn):
            await self.repo.revoke_refresh_token(token_hash)

            access_token = create_access_token(
                subject=user["id"],
                role=user["role"],
                institution_id=user.get("institution_id"),
            )
            raw_refresh, hashed_refresh = generate_refresh_token()
            expires_at = create_refresh_token_expiry()

            await self.repo.insert_refresh_token(
                token_id=uuid.uuid4(),
                user_id=user["id"],
                token_hash=hashed_refresh,
                expires_at=expires_at,
            )

        return TokenResponse(
            access_token=access_token,
            refresh_token=raw_refresh,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def logout(self, raw_token: str) -> None:
        """Revoke the provided refresh token."""
        token_hash = hash_refresh_token(raw_token)
        await self.repo.revoke_refresh_token(token_hash)
