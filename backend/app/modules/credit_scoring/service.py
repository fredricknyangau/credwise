"""
Credit scoring service.
"""
from __future__ import annotations

import uuid
from uuid import UUID

from asyncpg import Connection

from app.core.exceptions import BadRequestException
from app.modules.credit_scoring.engine import compute_score
from app.modules.credit_scoring.repository import CreditScoringRepository
from app.modules.credit_scoring.schemas import CreditScoreRead


class CreditScoringService:
    def __init__(self, conn: Connection) -> None:
        self.repo = CreditScoringRepository(conn)

    async def generate_score(self, user_id: UUID) -> CreditScoreRead:
        """
        Pulls all signals, runs the scoring engine, and persists the result.
        A new score record is created each time — history is preserved.
        """
        raw = await self.repo.get_scoring_inputs(user_id)
        if not raw:
            raise BadRequestException(
                "Cannot generate score: complete your financial profile and literacy modules first."
            )

        result = compute_score(raw)

        row = await self.repo.insert_score(
            score_id=uuid.uuid4(),
            user_id=user_id,
            score=result.score,
            rating=result.rating,
            literacy_weight=result.literacy_weight,
            savings_weight=result.savings_weight,
            stability_weight=result.stability_weight,
            repayment_weight=result.repayment_weight,
            cooperative_weight=result.cooperative_weight,
            factors=result.factors,
        )
        return CreditScoreRead(**row)

    async def get_latest_score(self, user_id: UUID) -> CreditScoreRead | None:
        row = await self.repo.get_latest_score(user_id)
        return CreditScoreRead(**row) if row else None
