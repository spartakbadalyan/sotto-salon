"""identity accounts, sessions, and scoped role grants

Revision ID: 0002_identity
Revises: 0001_baseline
Create Date: 2026-09-13
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_identity"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None

account_kind = sa.Enum("advertiser", "staff", name="accountkind", native_enum=False)
account_status = sa.Enum(
    "pending_verification",
    "active",
    "suspended",
    "closed",
    name="accountstatus",
    native_enum=False,
)
staff_role = sa.Enum(
    "moderator",
    "appeals",
    "billing_support",
    "security",
    name="staffrole",
    native_enum=False,
)
grant_action = sa.Enum("granted", "revoked", name="rolegrantaction", native_enum=False)


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    ]


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("normalized_email", sa.String(320), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("kind", account_kind, nullable=False),
        sa.Column("status", account_status, nullable=False),
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mfa_enrolled", sa.Boolean(), nullable=False),
        sa.Column("sessions_revoked_after", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_table(
        "account_sessions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "account_id",
            sa.String(64),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_digest", sa.String(64), nullable=False, unique=True),
        sa.Column("csrf_digest", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mfa_verified", sa.Boolean(), nullable=False),
        *_timestamps(),
    )
    op.create_index("ix_account_sessions_account_id", "account_sessions", ["account_id"])
    op.create_index(
        "ix_account_sessions_account_active", "account_sessions", ["account_id", "revoked_at"]
    )
    op.create_table(
        "role_grants",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "account_id",
            sa.String(64),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", staff_role, nullable=False),
        sa.Column(
            "granted_by_account_id",
            sa.String(64),
            sa.ForeignKey("accounts.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("reason", sa.String(500), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_role_grants_account_id", "role_grants", ["account_id"])
    op.create_index("ix_role_grants_account_active", "role_grants", ["account_id", "revoked_at"])
    op.create_table(
        "role_grant_audit",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "role_grant_id",
            sa.String(64),
            sa.ForeignKey("role_grants.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "actor_account_id",
            sa.String(64),
            sa.ForeignKey("accounts.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("action", grant_action, nullable=False),
        sa.Column("reason", sa.String(500), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_role_grant_audit_role_grant_id", "role_grant_audit", ["role_grant_id"])


def downgrade() -> None:
    op.drop_table("role_grant_audit")
    op.drop_table("role_grants")
    op.drop_table("account_sessions")
    op.drop_table("accounts")
