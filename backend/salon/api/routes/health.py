"""Liveness and readiness endpoints.

``/health/live`` reports the process is up. ``/health/ready`` additionally checks the
database connection. Neither returns secrets.
"""

from __future__ import annotations

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel
from sqlalchemy import text

from salon.core.db import create_db_engine

router = APIRouter(tags=["health"])


class LiveResponse(BaseModel):
    status: str


class ReadyResponse(BaseModel):
    status: str
    database: str


@router.get("/health/live", response_model=LiveResponse)
def live() -> LiveResponse:
    return LiveResponse(status="ok")


@router.get("/health/ready", response_model=ReadyResponse)
def ready(request: Request, response: Response) -> ReadyResponse:
    settings = request.app.state.settings
    try:
        engine = create_db_engine(settings)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return ReadyResponse(status="ok", database="ok")
    except Exception:
        # Do not leak connection strings or driver errors to the caller.
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadyResponse(status="degraded", database="unavailable")
