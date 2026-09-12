"""Shared test fixtures.

Tests construct :class:`Settings` explicitly rather than reading the ambient environment,
so they are hermetic and never depend on a developer's ``.env``.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from salon.api.app import create_app
from salon.core.config import Environment, Settings

SYNTHETIC_DSN = "postgresql+psycopg://salon:salon@127.0.0.1:5432/salon"


def make_settings(**overrides) -> Settings:
    base = dict(
        environment=Environment.development,
        database_url=SYNTHETIC_DSN,
        session_secret="test-secret",
    )
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


@pytest.fixture
def settings() -> Settings:
    return make_settings()


@pytest.fixture
def client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings))
