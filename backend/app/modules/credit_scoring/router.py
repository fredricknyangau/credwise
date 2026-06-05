"""
Credit scoring router.
"""
from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends

from app.core.database import get_connection
from app.core.dependencies import ClientDep, MfiAdminDep
from app.modules.credit_scoring.schemas import CreditScoreRead
from app.modules.credit_scoring.service import CreditScoringService
from app.shared.responses import APIResponse

router = APIRouter(prefix="/credit-scores", tags=["Credit Readiness"])


def _svc(conn: Connection = Depends(get_connection)) -> CreditScoringService:
    return CreditScoringService(conn)


@router.post(
    "/generate",
    response_model=APIResponse[CreditScoreRead],
    summary="Generate a new credit readiness score for the current user",
)
async def generate_score(
    current_user: ClientDep,
    svc: CreditScoringService = Depends(_svc),
) -> APIResponse[CreditScoreRead]:
    score = await svc.generate_score(current_user.user_id)
    return APIResponse.ok(score, "Score generated successfully")


@router.get(
    "/me",
    response_model=APIResponse[CreditScoreRead | None],
    summary="Get current user's latest credit readiness score",
)
async def get_my_score(
    current_user: ClientDep,
    svc: CreditScoringService = Depends(_svc),
) -> APIResponse[CreditScoreRead | None]:
    score = await svc.get_latest_score(current_user.user_id)
    return APIResponse.ok(score)


@router.get(
    "/{user_id}",
    response_model=APIResponse[CreditScoreRead | None],
    summary="MFI admin: view a client's latest credit readiness score",
)
async def get_client_score(
    user_id: UUID,
    _admin: MfiAdminDep,
    svc: CreditScoringService = Depends(_svc),
) -> APIResponse[CreditScoreRead | None]:
    score = await svc.get_latest_score(user_id)
    return APIResponse.ok(score)
