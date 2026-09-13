"""Minimal authenticated account API (SAL-009 initial slice)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from salon.core.config import Settings
from salon.identity.authorization import Principal
from salon.identity.dependencies import get_current_principal, get_db
from salon.identity.models import AccountKind, AccountSession, StaffRole
from salon.identity.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    revoke_session,
    validate_csrf,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


class CurrentUserResponse(BaseModel):
    account_id: str
    account_kind: AccountKind
    roles: list[StaffRole]
    mfa_verified: bool


@router.get("/me", response_model=CurrentUserResponse)
def current_user(
    principal: Annotated[Principal, Depends(get_current_principal)],
) -> CurrentUserResponse:
    return CurrentUserResponse(
        account_id=principal.account_id,
        account_kind=principal.kind,
        roles=sorted(principal.roles, key=lambda role: role.value),
        mfa_verified=principal.mfa_verified,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
    csrf_token: Annotated[str | None, Header(alias=CSRF_HEADER_NAME)] = None,
    session_token: Annotated[str | None, Cookie(alias=SESSION_COOKIE_NAME)] = None,
) -> None:
    # Reload the authenticated session to bind CSRF validation to this exact cookie.
    account_session = db.get(AccountSession, principal.session_id)
    settings: Settings = request.app.state.settings
    if (
        account_session is None
        or session_token is None
        or csrf_token is None
        or not validate_csrf(
            account_session, csrf_token, settings.session_secret.get_secret_value()
        )
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    revoke_session(db, principal.session_id)
    db.commit()
    response.delete_cookie(
        SESSION_COOKIE_NAME,
        httponly=True,
        secure=settings.environment.is_production,
        samesite="strict",
        path="/",
    )
