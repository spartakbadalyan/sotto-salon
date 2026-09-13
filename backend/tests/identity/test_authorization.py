from __future__ import annotations

import pytest
from fastapi import HTTPException

from salon.identity.authorization import (
    Permission,
    Principal,
    require_account_owner,
    require_staff_permission,
)
from salon.identity.models import AccountKind, StaffRole


def principal(
    *,
    account_id: str = "acct_owner",
    kind: AccountKind = AccountKind.advertiser,
    roles: frozenset[StaffRole] = frozenset(),
    mfa_verified: bool = False,
) -> Principal:
    return Principal(
        account_id=account_id,
        session_id="sess_test",
        kind=kind,
        roles=roles,
        mfa_verified=mfa_verified,
    )


def test_advertiser_can_access_only_owned_record() -> None:
    require_account_owner(principal(), "acct_owner")
    with pytest.raises(HTTPException) as exc:
        require_account_owner(principal(), "acct_someone_else")
    # Conceal another advertiser's private record instead of confirming it exists.
    assert exc.value.status_code == 404


def test_staff_without_mfa_cannot_use_privileged_permission() -> None:
    actor = principal(
        kind=AccountKind.staff,
        roles=frozenset({StaffRole.moderator}),
        mfa_verified=False,
    )
    with pytest.raises(HTTPException) as exc:
        require_staff_permission(actor, Permission.moderation_decide)
    assert exc.value.status_code == 403


def test_staff_roles_are_separate_and_require_explicit_permission() -> None:
    moderator = principal(
        kind=AccountKind.staff,
        roles=frozenset({StaffRole.moderator}),
        mfa_verified=True,
    )
    require_staff_permission(moderator, Permission.moderation_decide)
    with pytest.raises(HTTPException) as exc:
        require_staff_permission(moderator, Permission.appeals_decide)
    assert exc.value.status_code == 403

    billing = principal(
        kind=AccountKind.staff,
        roles=frozenset({StaffRole.billing_support}),
        mfa_verified=True,
    )
    require_staff_permission(billing, Permission.billing_support)
    with pytest.raises(HTTPException):
        require_staff_permission(billing, Permission.security_accounts)
