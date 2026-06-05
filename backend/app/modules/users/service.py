"""
User service.
"""
from __future__ import annotations

import uuid

from asyncpg import Connection

from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.core.security import hash_password
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import CreateClientRequest, UserRead
from app.shared.pagination import PaginatedResponse, PaginationParams


class UserService:
    def __init__(self, conn: Connection) -> None:
        self.repo = UserRepository(conn)

    async def create_client(
        self,
        payload: CreateClientRequest,
        institution_id: uuid.UUID,
    ) -> UserRead:
        if await self.repo.phone_exists(payload.phone_number):
            raise AlreadyExistsException("User with this phone number")

        user_id = uuid.uuid4()
        row = await self.repo.insert_client(
            user_id=user_id,
            institution_id=institution_id,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
            password_hash=hash_password(payload.password),
        )
        return UserRead(**row)

    async def get_user(self, user_id: uuid.UUID) -> UserRead:
        row = await self.repo.get_by_id(user_id)
        if not row:
            raise NotFoundException("User")
        return UserRead(**row)

    async def list_institution_clients(
        self,
        institution_id: uuid.UUID,
        params: PaginationParams,
    ) -> PaginatedResponse[UserRead]:
        total = await self.repo.count_by_institution(institution_id)
        rows = await self.repo.list_by_institution(
            institution_id, params.limit, params.offset
        )
        items = [UserRead(**r) for r in rows]
        return PaginatedResponse.build(items, total, params)

    async def update_status(
        self, user_id: uuid.UUID, is_active: bool
    ) -> UserRead:
        row = await self.repo.update_status(user_id, is_active)
        if not row:
            raise NotFoundException("User")
        # Reload full record
        return await self.get_user(user_id)
