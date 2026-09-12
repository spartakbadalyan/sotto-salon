"""Application error types.

``ConfigurationError`` deliberately renders *only* field locations and validation
messages, never the offending input values, so that a misconfiguration cannot leak a
secret (a bad ``SALON_SESSION_SECRET`` or a DSN with an embedded password) into logs,
tracebacks, or a crash report. This satisfies SAL-007-AC03 (missing settings fail with
redacted diagnostics).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


class SalonError(Exception):
    """Base class for application-level errors."""


class ConfigurationError(SalonError):
    """Raised when application settings are missing or invalid.

    The message lists the environment variable name and the validation message for
    each problem. Input values are never included.
    """

    def __init__(self, problems: Iterable[str]) -> None:
        self.problems = list(problems)
        body = "\n".join(f"  - {p}" for p in self.problems)
        super().__init__(
            "Invalid application configuration; values are redacted:\n" + body
        )

    @classmethod
    def from_validation_error(cls, exc: Any, env_prefix: str) -> ConfigurationError:
        """Build from a pydantic ``ValidationError`` without echoing any input."""
        problems: list[str] = []
        for error in exc.errors():
            loc = error.get("loc", ())
            field = str(loc[0]) if loc else "<root>"
            env_name = f"{env_prefix}{field.upper()}" if loc else "<configuration>"
            message = error.get("msg", "invalid value")
            problems.append(f"{env_name}: {message}")
        return cls(problems)
