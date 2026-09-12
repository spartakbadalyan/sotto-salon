"""Database engine, session factory, and shared ORM conventions.

Conventions (SAL-007-AC02): every table uses an opaque string primary key (never a
guessable sequential integer exposed to clients) and timezone-aware UTC timestamps.
``new_id`` mints prefixed opaque identifiers so IDs are self-describing in logs without
revealing counts or ordering.
"""

from __future__ import annotations

import secrets
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from salon.core.config import Settings

# Crockford-style base32 alphabet (no I/L/O/U) for readable opaque IDs.
_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def new_id(prefix: str, length: int = 26) -> str:
    """Return an opaque identifier such as ``acct_3F7K...`` (prefix + random suffix)."""
    body = "".join(secrets.choice(_ALPHABET) for _ in range(length))
    return f"{prefix}_{body}"


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SystemMetadata(Base, TimestampMixin):
    """Infrastructure-only key/value table.

    Present so the baseline migration has something to create and so the opaque-ID and
    UTC-timestamp conventions are exercised. It holds no customer data.
    """

    __tablename__ = "system_metadata"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(512), nullable=False)


def create_db_engine(settings: Settings, connect_timeout: int = 5) -> Engine:
    # A bounded connect timeout keeps the readiness endpoint (and tests without a live
    # database) from hanging when Postgres is unreachable.
    return create_engine(
        str(settings.database_url),
        pool_pre_ping=True,
        future=True,
        connect_args={"connect_timeout": connect_timeout},
    )


def create_session_factory(settings: Settings) -> sessionmaker:
    return sessionmaker(
        bind=create_db_engine(settings), expire_on_commit=False, future=True
    )
