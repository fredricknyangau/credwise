"""
Database connection pool management using asyncpg directly (no ORM).

Pool is created on application startup and torn down on shutdown.
Every request gets a connection from the pool via FastAPI's Depends().
Transactions are explicit: BEGIN → business logic → COMMIT/ROLLBACK.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from asyncpg import Connection, Pool

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# Module-level pool — initialised in lifespan
_pool: Pool | None = None


async def create_pool() -> Pool:
    """Create the asyncpg connection pool on startup."""
    settings = get_settings()
    pool = await asyncpg.create_pool(
        dsn=settings.asyncpg_dsn,
        min_size=settings.db_min_size,
        max_size=settings.db_max_size,
        max_inactive_connection_lifetime=settings.db_max_inactive_conn_lifetime,
        command_timeout=60,
        server_settings={"application_name": settings.app_name},
    )
    logger.info(
        "asyncpg pool created | min=%d max=%d",
        settings.db_min_size,
        settings.db_max_size,
    )
    return pool


async def close_pool() -> None:
    """Gracefully close the pool on shutdown."""
    global _pool
    if _pool is not None:
        await _pool.close()
        logger.info("asyncpg pool closed")
        _pool = None


def set_pool(pool: Pool) -> None:
    global _pool
    _pool = pool


def get_pool() -> Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialised. Check lifespan.")
    return _pool


# ---------------------------------------------------------------------------
# FastAPI dependency — injects a single connection per request
# ---------------------------------------------------------------------------

async def get_connection() -> AsyncGenerator[Connection, None]:
    """
    Yields a single asyncpg connection from the pool.

    Usage in route handlers::

        async def my_route(conn: Connection = Depends(get_connection)):
            ...
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn


# ---------------------------------------------------------------------------
# Transaction context manager for service-layer use
# ---------------------------------------------------------------------------

@asynccontextmanager
async def transaction(conn: Connection) -> AsyncGenerator[Connection, None]:
    """
    Wraps a block of database operations in an explicit transaction.

    Automatically COMMITs on success and ROLLBACKs on any exception.

    Usage::

        async with transaction(conn) as conn:
            await repo.insert_user(...)
            await repo.insert_profile(...)
    """
    async with conn.transaction():
        yield conn
