"""
Quiz schemas.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateQuizRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)


class QuizRead(BaseModel):
    id: UUID
    module_id: UUID
    title: str
    created_at: datetime


class CreateQuestionRequest(BaseModel):
    question: str = Field(..., min_length=5)
    options: list[str] = Field(..., min_length=2, max_length=6)
    correct_answer: str


class QuestionRead(BaseModel):
    id: UUID
    quiz_id: UUID
    question: str
    options: list[str]
    correct_answer: str
    created_at: datetime


class QuestionPublic(BaseModel):
    """Question shown to clients — correct_answer hidden."""
    id: UUID
    quiz_id: UUID
    question: str
    options: list[str]


class SubmitQuizRequest(BaseModel):
    answers: dict[str, str]  # question_id → chosen_answer


class QuizAttemptResult(BaseModel):
    id: UUID
    quiz_id: UUID
    score: float
    total_questions: int
    correct: int
    completed_at: datetime
    per_question: list[dict]


class QuizAttemptRead(BaseModel):
    id: UUID
    user_id: UUID
    quiz_id: UUID
    score: float
    completed_at: datetime
