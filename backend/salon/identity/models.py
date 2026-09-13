"""Persistence models for accounts, sessions, and scoped staff role grants."""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from salon.core.db import Base, TimestampMixin, new_id, utcnow


class AccountKind(enum.StrEnum):
    advertiser = "advertiser"
    staff = "staff"


class AccountStatus(enum.StrEnum):
    pending_verification = "pending_verification"
    active = "active"
    suspended = "suspended"
    closed = "closed"


class StaffRole(enum.StrEnum):
    moderator = "moderator"
    appeals = "appeals"
    billing_support = "billing_support"
    security = "security"


class RoleGrantAction(enum.StrEnum):
    granted = "granted"
    revoked = "revoked"


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("acct"))
    normalized_email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[AccountKind] = mapped_column(
        Enum(AccountKind, native_enum=False, length=32), nullable=False
    )
    status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus, native_enum=False, length=32),
        nullable=False,
        default=AccountStatus.pending_verification,
    )
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    mfa_enrolled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sessions_revoked_after: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class AccountSession(Base, TimestampMixin):
    __tablename__ = "account_sessions"
    __table_args__ = (Index("ix_account_sessions_account_active", "account_id", "revoked_at"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("sess"))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Tokens are never stored. This is HMAC-SHA256(raw token, application secret).
    token_digest: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    csrf_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mfa_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class RoleGrant(Base, TimestampMixin):
    __tablename__ = "role_grants"
    __table_args__ = (Index("ix_role_grants_account_active", "account_id", "revoked_at"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("grant"))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[StaffRole] = mapped_column(
        Enum(StaffRole, native_enum=False, length=32), nullable=False
    )
    granted_by_account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False
    )
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RoleGrantAudit(Base):
    """Append-only evidence for security-sensitive grant changes."""

    __tablename__ = "role_grant_audit"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("audit"))
    role_grant_id: Mapped[str] = mapped_column(
        ForeignKey("role_grants.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    actor_account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False
    )
    action: Mapped[RoleGrantAction] = mapped_column(
        Enum(RoleGrantAction, native_enum=False, length=16), nullable=False
    )
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )
