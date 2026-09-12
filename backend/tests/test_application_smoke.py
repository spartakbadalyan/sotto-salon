"""Application smoke tests (SAL-007-AC01/AC02 partial)."""

from __future__ import annotations

from salon import __version__


def test_liveness(client) -> None:
    resp = client.get("/health/live")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_meta_reports_non_secret_metadata(client) -> None:
    resp = client.get("/api/v1/meta")
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "sotto-salon"
    assert body["version"] == __version__
    assert body["environment"] == "development"
    assert body["verification_adapter"] == "synthetic"
    # No secret material is exposed.
    assert "session_secret" not in body
    assert "database_url" not in body


class _FakeConn:
    def __enter__(self) -> _FakeConn:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def execute(self, *args: object, **kwargs: object) -> None:
        return None


class _FakeEngine:
    def connect(self) -> _FakeConn:
        return _FakeConn()

    def dispose(self) -> None:
        return None


def test_readiness_degrades_when_database_unavailable(client, monkeypatch) -> None:
    # Force a connection failure so this negative path is deterministic regardless of
    # whether a local Postgres happens to be running. Response must be 503 and must not
    # leak the connection string.
    def boom(*args: object, **kwargs: object):
        raise RuntimeError("simulated database outage")

    monkeypatch.setattr("salon.api.routes.health.create_db_engine", boom)
    resp = client.get("/health/ready")
    assert resp.status_code == 503
    assert resp.json() == {"status": "degraded", "database": "unavailable"}


def test_readiness_ok_when_database_reachable(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "salon.api.routes.health.create_db_engine", lambda *a, **k: _FakeEngine()
    )
    resp = client.get("/health/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "database": "ok"}


def test_cors_allows_configured_origin(client) -> None:
    resp = client.get("/api/v1/meta", headers={"Origin": "http://localhost:3000"})
    assert resp.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_blocks_unknown_origin(client) -> None:
    resp = client.get("/api/v1/meta", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in resp.headers


def test_openapi_export_is_deterministic() -> None:
    import json

    from salon.api.app import create_app
    from tests.conftest import make_settings

    schema_a = json.dumps(create_app(make_settings()).openapi(), sort_keys=True)
    schema_b = json.dumps(create_app(make_settings()).openapi(), sort_keys=True)
    assert schema_a == schema_b
