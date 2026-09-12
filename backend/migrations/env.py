"""Alembic environment.

The database URL comes from application settings, not from alembic.ini, so credentials
never live in a tracked file. Target metadata is the shared declarative Base.
"""

from __future__ import annotations

import os

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import model modules so their tables register on Base.metadata.
from salon.core import db as _db  # noqa: F401
from salon.core.config import load_settings
from salon.core.db import Base

config = context.config
target_metadata = Base.metadata


def _database_url() -> str:
    # Precedence: `alembic -x db_url=...`, then SALON_MIGRATION_URL, then app settings.
    # The overrides let tests run against a throwaway SQLite database without loosening
    # the application's PostgresDsn requirement.
    x_args = context.get_x_argument(as_dictionary=True)
    if x_args.get("db_url"):
        return x_args["db_url"]
    override = os.environ.get("SALON_MIGRATION_URL")
    if override:
        return override
    return str(load_settings().database_url)


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section) or {}
    section["sqlalchemy.url"] = _database_url()
    connectable = engine_from_config(
        section, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
