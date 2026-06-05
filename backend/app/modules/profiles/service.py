"""
Profile service.
"""
from __future__ import annotations

import uuid
from uuid import UUID

from asyncpg import Connection

from app.core.exceptions import NotFoundException
from app.modules.profiles.repository import ProfileRepository
from app.modules.profiles.schemas import ProfileRead, UpsertProfileRequest


class ProfileService:
    def __init__(self, conn: Connection) -> None:
        self.repo = ProfileRepository(conn)

    async def upsert_profile(
        self, user_id: UUID, payload: UpsertProfileRequest
    ) -> ProfileRead:
        existing = await self.repo.get_by_user(user_id)
        profile_id = existing["id"] if existing else uuid.uuid4()
        row = await self.repo.upsert(
            profile_id=profile_id,
            user_id=user_id,
            monthly_income=payload.monthly_income,
            savings_frequency=payload.savings_frequency,
            business_type=payload.business_type,
            years_in_business=payload.years_in_business,
            cooperative_member=payload.cooperative_member,
            existing_loans=payload.existing_loans,
        )
        return ProfileRead(**row)

    async def get_profile(self, user_id: UUID) -> ProfileRead:
        row = await self.repo.get_by_user(user_id)
        if not row:
            raise NotFoundException("Financial profile")
        return ProfileRead(**row)
