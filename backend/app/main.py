"""
FastAPI application factory.

Responsibilities:
- Configure lifespan (pool creation + teardown)
- Register all module routers
- Add CORS, rate limiting, and global exception handlers
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import close_pool, create_pool, set_pool
from app.core.exceptions import DatabaseException
from app.core.logging import configure_logging

# Routers
from app.modules.analytics.router import router as analytics_router
from app.modules.auth.router import router as auth_router
from app.modules.credit_scoring.router import router as credit_router
from app.modules.institutions.router import router as institutions_router
from app.modules.literacy.router import router as literacy_router
from app.modules.profiles.router import router as profiles_router
from app.modules.quizzes.router import router as quizzes_router
from app.modules.users.router import router as users_router

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create the DB pool on startup; close it on shutdown."""
    logger.info("Starting %s v%s [%s]", settings.app_name, settings.app_version, settings.environment)
    pool = await create_pool()
    set_pool(pool)
    yield
    await close_pool()
    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Credwise — Financial literacy and ethical credit-readiness platform "
            "for MFIs and unbanked individuals."
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # ── Global exception handlers ─────────────────────────────────────────────

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(
        request: Request, exc: DatabaseException
    ) -> JSONResponse:
        logger.error("DatabaseException: %s | path=%s", exc.message, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"success": False, "message": "Database error", "detail": exc.message},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception | path=%s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": "Internal server error"},
        )

    # ── Routers ───────────────────────────────────────────────────────────────
    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(users_router, prefix=api_prefix)
    app.include_router(institutions_router, prefix=api_prefix)
    app.include_router(literacy_router, prefix=api_prefix)
    app.include_router(quizzes_router, prefix=api_prefix)
    app.include_router(profiles_router, prefix=api_prefix)
    app.include_router(credit_router, prefix=api_prefix)
    app.include_router(analytics_router, prefix=api_prefix)

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
