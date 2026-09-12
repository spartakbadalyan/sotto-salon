"""Application settings.

Configuration is read from ``SALON_``-prefixed environment variables (and an optional
``.env`` outside production). Two safety properties are enforced here:

* SAL-007-AC03 — missing or invalid settings raise :class:`ConfigurationError`, whose
  message names the offending variables but redacts every value.
* SAL-007-AC04 — a ``production`` environment refuses synthetic verification/payment
  adapters and authentication bypasses, so a real deployment cannot silently run on
  stand-ins that never contact a provider.
"""

from __future__ import annotations

import enum
import json
import os
from functools import lru_cache
from typing import Annotated

from pydantic import PostgresDsn, SecretStr, ValidationError, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from salon.core.errors import ConfigurationError

ENV_PREFIX = "SALON_"

# Loaded for local development/staging so the documented `cp .env.example .env` flow works.
# Production never reads a dotenv file (see :func:`load_settings`); it uses real env vars.
ENV_FILE = ".env"

DEFAULT_WEB_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Adapter identifiers that are local stand-ins only. They must never run in production.
SYNTHETIC_ADAPTERS = frozenset({"synthetic", "fake", "stub", "dummy", "memory", "none"})


class Environment(enum.StrEnum):
    development = "development"
    staging = "staging"
    production = "production"

    @property
    def is_production(self) -> bool:
        return self is Environment.production


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        env_file=None,
        extra="ignore",
        case_sensitive=False,
    )

    environment: Environment = Environment.development

    database_url: PostgresDsn
    session_secret: SecretStr

    verification_adapter: str = "synthetic"
    payment_adapter: str = "synthetic"

    # Browser origins allowed to call the API (CORS). Accepts a comma-separated string or
    # a JSON list from the environment. NoDecode disables pydantic-settings' automatic
    # JSON decoding of this list field so a plain comma-separated env value does not raise
    # a SettingsError before our validator runs.
    cors_allowed_origins: Annotated[list[str], NoDecode] = DEFAULT_WEB_ORIGINS

    # An explicit bypass is only ever honoured outside production (see validator).
    allow_auth_bypass: bool = False

    @field_validator("database_url", mode="before")
    @classmethod
    def _require_psycopg_driver(cls, value: object) -> object:
        # Only psycopg 3 is installed. Normalize a bare postgres scheme to it so a
        # standard postgresql:// URL does not fall back to (absent) psycopg2, and reject
        # an explicitly chosen unsupported driver rather than fail obscurely at connect.
        if isinstance(value, str):
            text = value.strip()
            for bare in ("postgresql://", "postgres://"):
                if text.startswith(bare):
                    return "postgresql+psycopg://" + text[len(bare):]
            if text.startswith("postgresql+") and not text.startswith("postgresql+psycopg://"):
                # Fixed message: never interpolate the input, which may carry credentials
                # (e.g. a malformed DSN with no "://" separator) into a diagnostic.
                raise ValueError(
                    "unsupported database driver; use the postgresql+psycopg:// scheme"
                )
        return value

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _parse_origins(cls, value: object) -> object:
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            if text.startswith("["):
                return json.loads(text)
            return [origin.strip() for origin in text.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def _forbid_synthetic_in_production(self) -> Settings:
        if not self.environment.is_production:
            return self
        offending: list[str] = []
        if self.verification_adapter.strip().lower() in SYNTHETIC_ADAPTERS:
            offending.append("verification_adapter")
        if self.payment_adapter.strip().lower() in SYNTHETIC_ADAPTERS:
            offending.append("payment_adapter")
        if self.allow_auth_bypass:
            offending.append("allow_auth_bypass")
        if offending:
            names = ", ".join(f"{ENV_PREFIX}{name.upper()}" for name in offending)
            raise ValueError(
                "production refuses synthetic adapters and authentication bypasses; "
                f"reconfigure: {names}"
            )
        return self

    def build_metadata(self) -> dict[str, str]:
        """Non-secret metadata safe to expose from health/meta endpoints."""
        return {
            "environment": self.environment.value,
            "verification_adapter": self.verification_adapter,
            "payment_adapter": self.payment_adapter,
        }


def load_settings() -> Settings:
    """Load settings, converting pydantic failures into redacted diagnostics.

    Outside production a local ``.env`` file is loaded (development convenience);
    production ignores any dotenv file and relies solely on real environment variables.
    """
    env = os.environ.get(f"{ENV_PREFIX}ENVIRONMENT", "development").strip().lower()
    env_file = None if env == Environment.production.value else ENV_FILE
    try:
        settings = Settings(_env_file=env_file)  # type: ignore[call-arg]
    except ValidationError as exc:
        raise ConfigurationError.from_validation_error(exc, ENV_PREFIX) from None
    # A dotenv file was loaded because the process environment did not select production.
    # If the resolved environment is nonetheless production, it was declared through the
    # dotenv file (or another non-process source); reject it so production can never draw
    # its credentials/secret from a dotenv file.
    if env_file is not None and settings.environment.is_production:
        raise ConfigurationError(
            [
                f"{ENV_PREFIX}ENVIRONMENT: production must be set in the process "
                "environment, not a dotenv file"
            ]
        )
    return settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
