"""FastAPI dependencies for database-backed session authentication."""

from __future__ import annotations

from collections.abc import Generator
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from salon.core.config import Settings
from salon.core.db import create_session_factory
from salon.identity.authorization import Principal
from salon.identity.sessions import SESSION_COOKIE_NAME, authenticate_session


def get_db(request: Request) -> Generator[Session, None, None]:
    factory = getattr(request.app.state, "session_factory", None)
    if factory is None:
        factory = create_session_factory(request.app.state.settings)
        request.app.state.session_factory = factory
    with factory() as db:
        yield db


def get_current_principal(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    session_token: Annotated[str | None, Cookie(alias=SESSION_COOKIE_NAME)] = None,
) -> Principal:
    # Keep every authentication failure identical to resist account/session enumeration.
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    settings: Settings = request.app.state.settings
    principal = authenticate_session(db, session_token, settings.session_secret.get_secret_value())
    if principal is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return principal
