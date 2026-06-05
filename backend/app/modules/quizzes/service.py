"""
Quiz service — grading logic lives here, not in the router.
"""
from __future__ import annotations

import uuid
from uuid import UUID

from asyncpg import Connection

from app.core.exceptions import BadRequestException, NotFoundException
from app.modules.quizzes.repository import QuizRepository
from app.modules.quizzes.schemas import (
    CreateQuestionRequest,
    CreateQuizRequest,
    QuestionPublic,
    QuestionRead,
    QuizAttemptResult,
    QuizRead,
    SubmitQuizRequest,
)


class QuizService:
    def __init__(self, conn: Connection) -> None:
        self.repo = QuizRepository(conn)

    async def create_quiz(self, module_id: UUID, payload: CreateQuizRequest) -> QuizRead:
        row = await self.repo.insert_quiz(uuid.uuid4(), module_id, payload.title)
        return QuizRead(**row)

    async def get_quiz(self, quiz_id: UUID) -> QuizRead:
        row = await self.repo.get_quiz_by_id(quiz_id)
        if not row:
            raise NotFoundException("Quiz")
        return QuizRead(**row)

    async def get_quiz_for_module(self, module_id: UUID) -> QuizRead:
        row = await self.repo.get_quiz_by_module(module_id)
        if not row:
            raise NotFoundException("Quiz for this module")
        return QuizRead(**row)

    async def add_question(
        self, quiz_id: UUID, payload: CreateQuestionRequest
    ) -> QuestionRead:
        await self.get_quiz(quiz_id)
        if payload.correct_answer not in payload.options:
            raise BadRequestException("correct_answer must be one of the provided options")
        row = await self.repo.insert_question(
            uuid.uuid4(), quiz_id, payload.question, payload.options, payload.correct_answer
        )
        return QuestionRead(**row)

    async def get_questions_for_client(self, quiz_id: UUID) -> list[QuestionPublic]:
        """Returns questions without correct_answer — for client-side display."""
        await self.get_quiz(quiz_id)
        rows = await self.repo.get_questions(quiz_id)
        return [QuestionPublic(**r) for r in rows]

    async def submit_quiz(
        self, user_id: UUID, quiz_id: UUID, payload: SubmitQuizRequest
    ) -> QuizAttemptResult:
        """
        Grading logic:
        1. Load all questions with their correct answers.
        2. Compare submitted answers against correct answers.
        3. Calculate score as percentage of correct answers.
        4. Persist the attempt.
        """
        await self.get_quiz(quiz_id)
        questions = await self.repo.get_questions(quiz_id)

        if not questions:
            raise BadRequestException("This quiz has no questions yet")

        per_question = []
        correct_count = 0

        for q_row in questions:
            q_id = str(q_row["id"])
            submitted = payload.answers.get(q_id)
            is_correct = submitted == q_row["correct_answer"]
            if is_correct:
                correct_count += 1
            per_question.append({
                "question_id": q_id,
                "submitted": submitted,
                "correct": q_row["correct_answer"],
                "is_correct": is_correct,
            })

        total = len(questions)
        score = round((correct_count / total) * 100, 2)

        attempt = await self.repo.insert_attempt(
            attempt_id=uuid.uuid4(),
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            answers=payload.answers,
        )

        return QuizAttemptResult(
            id=attempt["id"],
            quiz_id=attempt["quiz_id"],
            score=score,
            total_questions=total,
            correct=correct_count,
            completed_at=attempt["completed_at"],
            per_question=per_question,
        )
