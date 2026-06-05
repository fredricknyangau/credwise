"""
Literacy schemas.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateModuleRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=10)
    difficulty_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    estimated_minutes: int = Field(..., ge=1, le=300)


class ModuleRead(BaseModel):
    id: UUID
    title: str
    description: str
    difficulty_level: str
    estimated_minutes: int
    is_published: bool
    created_at: datetime


class CreateLessonRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    content: str = Field(..., min_length=50)
    lesson_order: int = Field(..., ge=1)


class LessonRead(BaseModel):
    id: UUID
    module_id: UUID
    title: str
    content: str
    lesson_order: int
    created_at: datetime


class ModuleProgress(BaseModel):
    module_id: UUID
    user_id: UUID
    total_lessons: int
    completed: int
    percentage: float


class ModuleProgressSummary(BaseModel):
    module_id: UUID
    title: str
    total_lessons: int
    completed: int
    percentage: float


class CompleteLesson(BaseModel):
    lesson_id: UUID
