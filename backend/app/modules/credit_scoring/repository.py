"""
Credit scoring repository.
"""
from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.credit_scoring import queries as q


class CreditScoringRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_scoring_inputs(self, user_id: UUID) -> dict[str, Any]:
        row = await self.conn.fetchrow(q.GET_SCORING_INPUTS, user_id)
        return dict(row) if row else {}

    async def insert_score(
        self,
        score_id: UUID,
        user_id: UUID,
        score: float,
        rating: str,
        literacy_weight: float,
        savings_weight: float,
        stability_weight: float,
        repayment_weight: float,
        cooperative_weight: float,
        factors: list[str],
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_SCORE,
            score_id,
            user_id,
            score,
            rating,
            literacy_weight,
            savings_weight,
            stability_weight,
            repayment_weight,
            cooperative_weight,
            json.dumps(factors),
        )
        d = dict(row)  # type: ignore[arg-type]
        if isinstance(d.get("factors"), str):
            d["factors"] = json.loads(d["factors"])
        return d

    async def get_latest_score(self, user_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_SCORE_BY_USER, user_id)
        if not row:
            return None
        d = dict(row)
        if isinstance(d.get("factors"), str):
            d["factors"] = json.loads(d["factors"])
        return d
