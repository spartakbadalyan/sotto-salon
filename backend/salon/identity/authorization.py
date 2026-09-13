"""Ownership and least-privilege authorization policy."""

from __future__ import annotations

import enum
from dataclasses import dataclass

from fastapi import HTTPException, status

from salon.identity.models import AccountKind, StaffRole


class Permission(enum.StrEnum):
    moderation_read = "moderation:read"
    moderation_decide = "moderation:decide"
    appeals_read = "appeals:read"
    appeals_decide = "appeals:decide"
    billing_read = "billing:read"
    billing_support = "billing:support"
    security_accounts = "security:accounts"
    security_roles = "security:roles"


ROLE_PERMISSIONS: dict[StaffRole, frozenset[Permission]] = {
    StaffRole.moderator: frozenset({Permission.moderation_read, Permission.moderation_decide}),
    StaffRole.appeals: frozenset({Permission.appeals_read, Permission.appeals_decide}),
    StaffRole.billing_support: frozenset({Permission.billing_read, Permission.billing_support}),
    StaffRole.security: frozenset({Permission.security_accounts, Permission.security_roles}),
}


@dataclass(frozen=True, slots=True)
class Principal:
    account_id: str
    session_id: str
    kind: AccountKind
    roles: frozenset[StaffRole]
    mfa_verified: bool


def require_account_owner(principal: Principal, owner_account_id: str) -> None:
    """Allow only the owning advertiser; conceal whether another account's record exists."""
    if principal.kind is not AccountKind.advertiser or principal.account_id != owner_account_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


def require_staff_permission(principal: Principal, permission: Permission) -> None:
    """Require staff MFA and one explicitly granted role containing the permission."""
    if principal.kind is not AccountKind.staff or not principal.mfa_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    effective = frozenset().union(
        *(ROLE_PERMISSIONS.get(role, frozenset()) for role in principal.roles)
    )
    if permission not in effective:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
