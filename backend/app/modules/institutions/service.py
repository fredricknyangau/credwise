"""
Institution service.
"""
from __future__ import annotations

from uuid import UUID

from asyncpg import Connection

from app.core.exceptions import NotFoundException
from app.modules.institutions.repository import InstitutionRepository
from app.modules.institutions.schemas import InstitutionRead, InstitutionSummary
from app.shared.pagination import PaginatedResponse, PaginationParams


class InstitutionService:
    def __init__(self, conn: Connection) -> None:
        self.repo = InstitutionRepository(conn)

    async def get_institution(self, institution_id: UUID) -> InstitutionRead:
        row = await self.repo.get_by_id(institution_id)
        if not row:
            raise NotFoundException("Institution")
        return InstitutionRead(**row)

    async def get_summary(self, institution_id: UUID) -> InstitutionSummary:
        row = await self.repo.get_summary(institution_id)
        if not row:
            raise NotFoundException("Institution")
        return InstitutionSummary(**row)

    async def list_institutions(
        self, params: PaginationParams
    ) -> PaginatedResponse[InstitutionRead]:
        total = await self.repo.count_all()
        rows = await self.repo.list_all(params.limit, params.offset)
        items = [InstitutionRead(**r) for r in rows]
        return PaginatedResponse.build(items, total, params)

    async def update_status(
        self, institution_id: UUID, is_active: bool
    ) -> InstitutionRead:
        row = await self.repo.update_status(institution_id, is_active)
        if not row:
            raise NotFoundException("Institution")
        return await self.get_institution(institution_id)
