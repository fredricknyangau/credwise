# Alembic environment configuration
# Uses raw SQL — no ORM models. asyncpg-compatible async setup.

from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Alembic Config object
config = context.config

# Override sqlalchemy.url from environment if present
db_url = os.getenv("DATABASE_URL", "")
if db_url:
    import re
    # Ensure asyncpg driver
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    db_url = db_url.replace("sslmode=", "ssl=")
    db_url = re.sub(r'([?&])channel_binding=[^&]*(&?)', r'\1', db_url)
    db_url = db_url.replace("?&", "?").rstrip("?&")
    config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None  # No ORM — migrations are pure SQL


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generate SQL script)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    url = config.get_main_option("sqlalchemy.url")
    engine = create_async_engine(url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
