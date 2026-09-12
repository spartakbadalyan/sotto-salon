"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from salon import __version__
from salon.api.routes import health, meta
from salon.core.adapters import assert_adapters_allowed
from salon.core.config import Settings, get_settings
from salon.core.logging import configure_logging

API_PREFIX = "/api/v1"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging()
    # Defence in depth: never start a production process on synthetic adapters.
    assert_adapters_allowed(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = settings
        yield

    app = FastAPI(
        title="Sotto Salon API",
        version=__version__,
        summary="Synthetic-only foundation (SAL-007).",
        lifespan=lifespan,
    )
    app.state.settings = settings
    # Allow the configured web origin(s) so the browser client can call the API.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(meta.router, prefix=API_PREFIX)
    return app
