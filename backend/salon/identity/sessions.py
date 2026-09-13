"""Opaque session issuance, authentication, CSRF validation, and revocation."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from salon.core.db import utcnow
from salon.identity.authorization import Principal
from salon.identity.models import (
    Account,
    AccountSession,
    AccountStatus,
    RoleGrant,
)

SESSION_COOKIE_NAME = "salon_session"
CSRF_HEADER_NAME = "X-CSRF-Token"
DEFAULT_SESSION_TTL = timedelta(hours=12)


def _digest(value: str, secret: str) -> str:
    return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()


def issue_session(
    db: Session,
    account: Account,
    secret: str,
    *,
    mfa_verified: bool = False,
    now: datetime | None = None,
) -> tuple[AccountSession, str, str]:
    """Persist a fresh session and return its one-time raw cookie and CSRF values."""
    if account.status is not AccountStatus.active:
        raise ValueError("cannot issue a session for an inactive account")
    now = now or utcnow()
    raw_token = secrets.token_urlsafe(32)
    raw_csrf = secrets.token_urlsafe(32)
    session = AccountSession(
        account_id=account.id,
        token_digest=_digest(raw_token, secret),
        csrf_digest=_digest(raw_csrf, secret),
        expires_at=now + DEFAULT_SESSION_TTL,
        mfa_verified=mfa_verified,
    )
    db.add(session)
    db.flush()
    return session, raw_token, raw_csrf


def _as_utc(value: datetime) -> datetime:
    # SQLite drops timezone metadata in tests; production Postgres preserves it.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def authenticate_session(
    db: Session,
    raw_token: str,
    secret: str,
    *,
    now: datetime | None = None,
) -> Principal | None:
    now = now or utcnow()
    row = db.execute(
        select(AccountSession, Account)
        .join(Account, Account.id == AccountSession.account_id)
        .where(AccountSession.token_digest == _digest(raw_token, secret))
    ).one_or_none()
    if row is None:
        return None
    session, account = row
    if (
        session.revoked_at is not None
        or _as_utc(session.expires_at) <= now
        or account.status is not AccountStatus.active
        or (
            account.sessions_revoked_after is not None
            and _as_utc(session.created_at) <= _as_utc(account.sessions_revoked_after)
        )
    ):
        return None

    roles = db.scalars(
        select(RoleGrant.role).where(
            RoleGrant.account_id == account.id,
            RoleGrant.revoked_at.is_(None),
        )
    ).all()
    return Principal(
        account_id=account.id,
        session_id=session.id,
        kind=account.kind,
        roles=frozenset(roles),
        # A stale/corrupt session flag can never substitute for current MFA enrollment.
        mfa_verified=session.mfa_verified and account.mfa_enrolled,
    )


def validate_csrf(session: AccountSession, raw_csrf: str, secret: str) -> bool:
    return hmac.compare_digest(session.csrf_digest, _digest(raw_csrf, secret))


def revoke_session(db: Session, session_id: str, *, now: datetime | None = None) -> None:
    db.execute(
        update(AccountSession)
        .where(AccountSession.id == session_id, AccountSession.revoked_at.is_(None))
        .values(revoked_at=now or utcnow())
    )


def revoke_all_sessions(db: Session, account_id: str, *, now: datetime | None = None) -> None:
    """Invalidate all existing sessions without waiting for cache or token expiry."""
    timestamp = now or utcnow()
    db.execute(
        update(Account).where(Account.id == account_id).values(sessions_revoked_after=timestamp)
    )
    db.execute(
        update(AccountSession)
        .where(AccountSession.account_id == account_id, AccountSession.revoked_at.is_(None))
        .values(revoked_at=timestamp)
    )
