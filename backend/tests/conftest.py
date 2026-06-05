"""
Shared test fixtures.

Uses a dedicated test database. Each test that touches the DB runs inside
a transaction that is rolled back after the test — ensures full isolation.
"""
from __future__ import annotations

import asyncio
import os
from typing import AsyncGenerator
from uuid import uuid4

import asyncpg
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Force test env before importing app modules
os.environ.setdefault("DATABASE_URL", "postgresql://credwise:credwise@localhost:5432/credwise_test")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("ENVIRONMENT", "development")

from app.core.database import set_pool
from app.core.security import hash_password, create_access_token
from app.main import app


# ── Event loop ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ── Database pool ─────────────────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session")
async def db_pool():
    pool = await asyncpg.create_pool(
        dsn=os.environ["DATABASE_URL"],
        min_size=2,
        max_size=5,
    )
    set_pool(pool)
    yield pool
    await pool.close()


@pytest_asyncio.fixture()
async def conn(db_pool):
    """
    Yields an asyncpg connection inside a transaction.
    The transaction is rolled back after each test — no cleanup needed.
    """
    async with db_pool.acquire() as connection:
        tr = connection.transaction()
        await tr.start()
        yield connection
        await tr.rollback()


# ── HTTP client ───────────────────────────────────────────────────────────────

@pytest_asyncio.fixture()
async def client(db_pool) -> AsyncGenerator[AsyncClient, None]:
    """httpx AsyncClient wired to the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


# ── Auth helpers ──────────────────────────────────────────────────────────────

@pytest.fixture()
def platform_admin_token() -> str:
    return create_access_token(
        subject=uuid4(), role="platform_admin"
    )


@pytest.fixture()
def mfi_admin_token(conn) -> str:
    inst_id = uuid4()
    return create_access_token(
        subject=uuid4(), role="mfi_admin", institution_id=inst_id
    )


@pytest.fixture()
def client_token() -> str:
    return create_access_token(
        subject=uuid4(), role="client", institution_id=uuid4()
    )
