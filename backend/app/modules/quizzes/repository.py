"""
Quiz repository.
"""
from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from asyncpg import Connection

from app.modules.quizzes import queries as q


class QuizRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_quiz_by_id(self, quiz_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_QUIZ_BY_ID, quiz_id)
        return dict(row) if row else None

    async def get_quiz_by_module(self, module_id: UUID) -> dict[str, Any] | None:
        row = await self.conn.fetchrow(q.GET_QUIZ_BY_MODULE, module_id)
        return dict(row) if row else None

    async def insert_quiz(
        self, quiz_id: UUID, module_id: UUID, title: str
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(q.INSERT_QUIZ, quiz_id, module_id, title)
        return dict(row)  # type: ignore[arg-type]

    async def get_questions(self, quiz_id: UUID) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.GET_QUESTIONS_BY_QUIZ, quiz_id)
        result = []
        for r in rows:
            d = dict(r)
            # asyncpg returns JSONB as string
            if isinstance(d.get("options"), str):
                d["options"] = json.loads(d["options"])
            result.append(d)
        return result

    async def insert_question(
        self,
        question_id: UUID,
        quiz_id: UUID,
        question: str,
        options: list[str],
        correct_answer: str,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_QUESTION,
            question_id,
            quiz_id,
            question,
            json.dumps(options),
            correct_answer,
        )
        d = dict(row)  # type: ignore[arg-type]
        if isinstance(d.get("options"), str):
            d["options"] = json.loads(d["options"])
        return d

    async def insert_attempt(
        self,
        attempt_id: UUID,
        user_id: UUID,
        quiz_id: UUID,
        score: float,
        answers: dict,
    ) -> dict[str, Any]:
        row = await self.conn.fetchrow(
            q.INSERT_QUIZ_ATTEMPT,
            attempt_id, user_id, quiz_id, score, json.dumps(answers),
        )
        return dict(row)  # type: ignore[arg-type]

    async def get_attempts(
        self, user_id: UUID, quiz_id: UUID
    ) -> list[dict[str, Any]]:
        rows = await self.conn.fetch(q.GET_ATTEMPTS_BY_USER_QUIZ, user_id, quiz_id)
        return [dict(r) for r in rows]

    async def get_best_score(self, user_id: UUID, quiz_id: UUID) -> float | None:
        row = await self.conn.fetchrow(q.GET_BEST_SCORE_FOR_USER_QUIZ, user_id, quiz_id)
        return float(row["best_score"]) if row and row["best_score"] is not None else None
