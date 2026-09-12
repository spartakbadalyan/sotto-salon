"""ASGI entrypoint: ``uvicorn salon.api.main:app``."""

from __future__ import annotations

from salon.api.app import create_app

app = create_app()
