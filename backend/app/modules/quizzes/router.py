"""
Quizzes router.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, status

from app.core.database import get_connection
from app.core.dependencies import ClientDep, MfiAdminDep
from app.modules.quizzes.schemas import (
    CreateQuestionRequest,
    CreateQuizRequest,
    QuestionPublic,
    QuestionRead,
    QuizAttemptResult,
    QuizRead,
    SubmitQuizRequest,
)
from app.modules.quizzes.service import QuizService
from app.shared.responses import APIResponse

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


def _svc(conn: Connection = Depends(get_connection)) -> QuizService:
    return QuizService(conn)


@router.post(
    "/modules/{module_id}",
    response_model=APIResponse[QuizRead],
    status_code=status.HTTP_201_CREATED,
    summary="MFI admin: create a quiz for a module",
)
async def create_quiz(
    module_id: UUID,
    payload: CreateQuizRequest,
    _admin: MfiAdminDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[QuizRead]:
    quiz = await svc.create_quiz(module_id, payload)
    return APIResponse.created(quiz)


@router.get(
    "/{quiz_id}",
    response_model=APIResponse[QuizRead],
    summary="Get quiz details",
)
async def get_quiz(
    quiz_id: UUID,
    _user: ClientDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[QuizRead]:
    quiz = await svc.get_quiz(quiz_id)
    return APIResponse.ok(quiz)


@router.get(
    "/modules/{module_id}",
    response_model=APIResponse[QuizRead],
    summary="Get quiz for a module",
)
async def get_quiz_for_module(
    module_id: UUID,
    _user: ClientDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[QuizRead]:
    quiz = await svc.get_quiz_for_module(module_id)
    return APIResponse.ok(quiz)


@router.post(
    "/{quiz_id}/questions",
    response_model=APIResponse[QuestionRead],
    status_code=status.HTTP_201_CREATED,
    summary="MFI admin: add a question to a quiz",
)
async def add_question(
    quiz_id: UUID,
    payload: CreateQuestionRequest,
    _admin: MfiAdminDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[QuestionRead]:
    question = await svc.add_question(quiz_id, payload)
    return APIResponse.created(question)


@router.get(
    "/{quiz_id}/questions",
    response_model=APIResponse[list[QuestionPublic]],
    summary="Get quiz questions (without correct answers)",
)
async def get_questions(
    quiz_id: UUID,
    _user: ClientDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[list[QuestionPublic]]:
    questions = await svc.get_questions_for_client(quiz_id)
    return APIResponse.ok(questions)


@router.post(
    "/{quiz_id}/submit",
    response_model=APIResponse[QuizAttemptResult],
    summary="Submit quiz answers and receive score",
)
async def submit_quiz(
    quiz_id: UUID,
    payload: SubmitQuizRequest,
    current_user: ClientDep,
    svc: QuizService = Depends(_svc),
) -> APIResponse[QuizAttemptResult]:
    result = await svc.submit_quiz(current_user.user_id, quiz_id, payload)
    return APIResponse.ok(result)
