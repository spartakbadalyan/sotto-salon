from __future__ import annotations

from collections.abc import Iterator
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from salon.api.app import create_app
from salon.core.db import Base, utcnow
from salon.identity.dependencies import get_db
from salon.identity.models import Account, AccountKind, AccountStatus, RoleGrant, StaffRole
from salon.identity.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    authenticate_session,
    issue_session,
    revoke_all_sessions,
)
from tests.conftest import make_settings


@pytest.fixture
def db() -> Iterator[Session]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session
    engine.dispose()


def make_account(
    db: Session,
    account_id: str = "acct_advertiser",
    *,
    kind: AccountKind = AccountKind.advertiser,
) -> Account:
    account = Account(
        id=account_id,
        normalized_email=f"{account_id}@example.invalid",
        # Authentication flows will replace this test-only sentinel with a password hasher.
        password_hash="not-a-real-password-hash",
        kind=kind,
        status=AccountStatus.active,
        email_verified_at=utcnow(),
        mfa_enrolled=kind is AccountKind.staff,
    )
    db.add(account)
    db.flush()
    return account


def make_client(db: Session) -> TestClient:
    app = create_app(make_settings())

    def override_db() -> Iterator[Session]:
        yield db

    app.dependency_overrides[get_db] = override_db
    return TestClient(app)


def test_current_user_uses_opaque_session_and_returns_minimal_identity(db: Session) -> None:
    account = make_account(db)
    _, raw_token, _ = issue_session(db, account, "test-secret")
    db.commit()
    client = make_client(db)
    client.cookies.set(SESSION_COOKIE_NAME, raw_token)

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "account_id": account.id,
        "account_kind": "advertiser",
        "roles": [],
        "mfa_verified": False,
    }
    assert raw_token not in response.text
    assert "normalized_email" not in response.text


def test_inactive_account_cannot_be_issued_a_session(db: Session) -> None:
    account = make_account(db)
    account.status = AccountStatus.pending_verification
    with pytest.raises(ValueError, match="inactive account"):
        issue_session(db, account, "test-secret")


def test_staff_session_loads_only_active_role_grants(db: Session) -> None:
    staff = make_account(db, "acct_staff", kind=AccountKind.staff)
    db.add_all(
        [
            RoleGrant(
                account_id=staff.id,
                role=StaffRole.moderator,
                granted_by_account_id=staff.id,
                reason="synthetic test assignment",
            ),
            RoleGrant(
                account_id=staff.id,
                role=StaffRole.security,
                granted_by_account_id=staff.id,
                reason="synthetic revoked assignment",
                revoked_at=utcnow(),
            ),
        ]
    )
    _, raw_token, _ = issue_session(db, staff, "test-secret", mfa_verified=True)
    db.commit()
    client = make_client(db)
    client.cookies.set(SESSION_COOKIE_NAME, raw_token)

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()["roles"] == ["moderator"]
    assert response.json()["mfa_verified"] is True


def test_session_flag_cannot_bypass_missing_staff_mfa_enrollment(db: Session) -> None:
    staff = make_account(db, "acct_staff", kind=AccountKind.staff)
    staff.mfa_enrolled = False
    _, raw_token, _ = issue_session(db, staff, "test-secret", mfa_verified=True)
    db.commit()

    principal = authenticate_session(db, raw_token, "test-secret")

    assert principal is not None
    assert principal.mfa_verified is False


def test_logout_requires_matching_csrf_and_revokes_immediately(db: Session) -> None:
    account = make_account(db)
    _, raw_token, raw_csrf = issue_session(db, account, "test-secret")
    db.commit()
    client = make_client(db)
    client.cookies.set(SESSION_COOKIE_NAME, raw_token)

    rejected = client.post("/api/v1/auth/logout", headers={CSRF_HEADER_NAME: "wrong-token"})
    assert rejected.status_code == 403
    assert client.get("/api/v1/auth/me").status_code == 200

    logged_out = client.post("/api/v1/auth/logout", headers={CSRF_HEADER_NAME: raw_csrf})
    assert logged_out.status_code == 204
    # Revocation takes effect on the next read, comfortably inside the 60-second bound.
    client.cookies.set(SESSION_COOKIE_NAME, raw_token)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_expired_suspended_and_globally_revoked_sessions_fail_identically(db: Session) -> None:
    account = make_account(db)
    now = utcnow()
    expired, expired_token, _ = issue_session(db, account, "test-secret", now=now)
    expired.expires_at = now - timedelta(seconds=1)
    db.commit()
    assert authenticate_session(db, expired_token, "test-secret", now=now) is None

    active, active_token, _ = issue_session(db, account, "test-secret", now=now)
    db.commit()
    account.status = AccountStatus.suspended
    db.commit()
    assert authenticate_session(db, active_token, "test-secret", now=now) is None

    account.status = AccountStatus.active
    db.commit()
    revoke_all_sessions(db, account.id, now=now + timedelta(seconds=1))
    db.commit()
    assert (
        authenticate_session(db, active_token, "test-secret", now=now + timedelta(seconds=2))
        is None
    )


def test_missing_and_unknown_session_have_same_public_failure(db: Session) -> None:
    client = make_client(db)
    missing = client.get("/api/v1/auth/me")
    client.cookies.set(SESSION_COOKIE_NAME, "unknown-high-entropy-token")
    unknown = client.get("/api/v1/auth/me")

    assert missing.status_code == unknown.status_code == 401
    assert missing.json() == unknown.json() == {"detail": "Unauthorized"}
