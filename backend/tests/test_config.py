"""Configuration safety tests (SAL-007-AC03 and AC04)."""

from __future__ import annotations

import pytest

from salon.core.adapters import assert_adapters_allowed
from salon.core.config import Environment, Settings, load_settings
from salon.core.errors import ConfigurationError
from tests.conftest import make_settings


def test_missing_settings_raise_redacted_diagnostics(monkeypatch, tmp_path) -> None:
    # Run in a clean directory so a developer's local .env cannot supply the missing value.
    monkeypatch.chdir(tmp_path)
    # A real, secret-looking value that must never appear in the diagnostics.
    secret = "super-secret-signing-key-value"
    monkeypatch.setenv("SALON_SESSION_SECRET", secret)
    monkeypatch.delenv("SALON_DATABASE_URL", raising=False)

    with pytest.raises(ConfigurationError) as excinfo:
        load_settings()

    message = str(excinfo.value)
    # Names the missing variable...
    assert "SALON_DATABASE_URL" in message
    # ...but never echoes the provided secret value.
    assert secret not in message


def test_production_rejects_synthetic_verification_adapter() -> None:
    with pytest.raises(ValueError) as excinfo:
        make_settings(
            environment=Environment.production,
            verification_adapter="synthetic",
            payment_adapter="ccbill",
        )
    assert "SALON_VERIFICATION_ADAPTER" in str(excinfo.value)


def test_production_rejects_synthetic_payment_adapter() -> None:
    with pytest.raises(ValueError) as excinfo:
        make_settings(
            environment=Environment.production,
            verification_adapter="yoti",
            payment_adapter="fake",
        )
    assert "SALON_PAYMENT_ADAPTER" in str(excinfo.value)


def test_production_rejects_auth_bypass() -> None:
    with pytest.raises(ValueError):
        make_settings(
            environment=Environment.production,
            verification_adapter="yoti",
            payment_adapter="ccbill",
            allow_auth_bypass=True,
        )


def test_production_accepts_real_adapters() -> None:
    settings = make_settings(
        environment=Environment.production,
        verification_adapter="yoti",
        payment_adapter="ccbill",
    )
    assert settings.environment.is_production
    # The runtime guard also passes for real adapters.
    assert_adapters_allowed(settings)


def test_runtime_guard_blocks_synthetic_production() -> None:
    # Bypass the model validator to simulate a drifted runtime, then prove the
    # defence-in-depth guard still fails closed.
    settings = make_settings(verification_adapter="yoti", payment_adapter="ccbill")
    object.__setattr__(settings, "environment", Environment.production)
    object.__setattr__(settings, "payment_adapter", "synthetic")
    with pytest.raises(RuntimeError):
        assert_adapters_allowed(settings)


def test_development_allows_synthetic() -> None:
    settings = make_settings()  # development defaults
    assert settings.verification_adapter == "synthetic"
    assert_adapters_allowed(settings)  # no-op outside production
    assert isinstance(settings, Settings)


def _write_dotenv(path) -> None:
    (path / ".env").write_text(
        "SALON_DATABASE_URL=postgresql+psycopg://salon:salon@127.0.0.1:5432/salon\n"
        "SALON_SESSION_SECRET=from-dotenv\n",
        encoding="utf-8",
    )


def test_dotenv_is_loaded_in_development(monkeypatch, tmp_path) -> None:
    _write_dotenv(tmp_path)
    monkeypatch.chdir(tmp_path)
    for key in ("SALON_DATABASE_URL", "SALON_SESSION_SECRET", "SALON_ENVIRONMENT"):
        monkeypatch.delenv(key, raising=False)
    settings = load_settings()
    assert settings.session_secret.get_secret_value() == "from-dotenv"


def test_dotenv_is_ignored_in_production(monkeypatch, tmp_path) -> None:
    # Real adapters via env so the only possible failure is the missing DB/secret,
    # proving production did not read the dotenv file.
    _write_dotenv(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SALON_ENVIRONMENT", "production")
    monkeypatch.setenv("SALON_VERIFICATION_ADAPTER", "yoti")
    monkeypatch.setenv("SALON_PAYMENT_ADAPTER", "ccbill")
    for key in ("SALON_DATABASE_URL", "SALON_SESSION_SECRET"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ConfigurationError):
        load_settings()


def test_cors_origins_accept_comma_separated_string() -> None:
    settings = make_settings(cors_allowed_origins="http://a.example, http://b.example")
    assert settings.cors_allowed_origins == ["http://a.example", "http://b.example"]


def test_example_dotenv_flow_loads_via_settings_source(monkeypatch, tmp_path) -> None:
    # Reproduces the documented `cp .env.example .env` startup: values must flow through
    # the real settings/env source (not the direct constructor), including a
    # comma-separated CORS list and a bare postgres scheme.
    (tmp_path / ".env").write_text(
        "SALON_ENVIRONMENT=development\n"
        "SALON_DATABASE_URL=postgresql://salon:salon@127.0.0.1:5432/salon\n"
        "SALON_SESSION_SECRET=dev-secret\n"
        "SALON_CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    for key in (
        "SALON_ENVIRONMENT",
        "SALON_DATABASE_URL",
        "SALON_SESSION_SECRET",
        "SALON_CORS_ALLOWED_ORIGINS",
    ):
        monkeypatch.delenv(key, raising=False)
    settings = load_settings()
    assert settings.cors_allowed_origins == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    assert str(settings.database_url).startswith("postgresql+psycopg://")


def test_cors_origins_accept_json_list() -> None:
    settings = make_settings(cors_allowed_origins='["http://a.example"]')
    assert settings.cors_allowed_origins == ["http://a.example"]


def test_bare_postgres_url_is_normalized_to_psycopg() -> None:
    settings = make_settings(
        database_url="postgresql://salon:salon@127.0.0.1:5432/salon"
    )
    assert str(settings.database_url).startswith("postgresql+psycopg://")


def test_unsupported_database_driver_is_rejected() -> None:
    with pytest.raises(ValueError):
        make_settings(
            database_url="postgresql+asyncpg://salon:salon@127.0.0.1:5432/salon"
        )


def test_production_cannot_be_selected_via_dotenv(monkeypatch, tmp_path) -> None:
    # Production declared inside .env (not the process env) with real adapters/secrets.
    (tmp_path / ".env").write_text(
        "SALON_ENVIRONMENT=production\n"
        "SALON_DATABASE_URL=postgresql+psycopg://salon:salon@127.0.0.1:5432/salon\n"
        "SALON_SESSION_SECRET=dotenv-secret\n"
        "SALON_VERIFICATION_ADAPTER=yoti\n"
        "SALON_PAYMENT_ADAPTER=ccbill\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    for key in (
        "SALON_ENVIRONMENT",
        "SALON_DATABASE_URL",
        "SALON_SESSION_SECRET",
        "SALON_VERIFICATION_ADAPTER",
        "SALON_PAYMENT_ADAPTER",
    ):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ConfigurationError) as excinfo:
        load_settings()
    message = str(excinfo.value)
    assert "SALON_ENVIRONMENT" in message
    assert "dotenv-secret" not in message


def test_production_via_process_env_is_accepted(monkeypatch, tmp_path) -> None:
    # No dotenv is read when the process environment selects production.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SALON_ENVIRONMENT", "production")
    monkeypatch.setenv(
        "SALON_DATABASE_URL", "postgresql+psycopg://salon:salon@127.0.0.1:5432/salon"
    )
    monkeypatch.setenv("SALON_SESSION_SECRET", "env-secret")
    monkeypatch.setenv("SALON_VERIFICATION_ADAPTER", "yoti")
    monkeypatch.setenv("SALON_PAYMENT_ADAPTER", "ccbill")
    settings = load_settings()
    assert settings.environment.is_production


def test_malformed_dsn_credentials_never_leak_into_diagnostics(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SALON_SESSION_SECRET", "x")
    # Malformed DSN (single slash, no "://") carrying a password.
    monkeypatch.setenv(
        "SALON_DATABASE_URL", "postgresql+psycopg:/user:TOPSECRET@localhost/db"
    )
    with pytest.raises(ConfigurationError) as excinfo:
        load_settings()
    assert "TOPSECRET" not in str(excinfo.value)
