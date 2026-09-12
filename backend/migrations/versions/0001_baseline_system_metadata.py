"""baseline system metadata

Revision ID: 0001_baseline
Revises:
Create Date: 2026-09-12

Establishes the opaque-ID + timezone-aware-UTC conventions on an infrastructure-only
table. No customer tables are created here.
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The unique constraint is declared inline (not a follow-up ALTER) so the migration
    # is portable to SQLite, which cannot drop constraints via ALTER.
    op.create_table(
        "system_metadata",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("value", sa.String(length=512), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("key", name="uq_system_metadata_key"),
    )


def downgrade() -> None:
    op.drop_table("system_metadata")
