"""Integration adapter selection.

The application talks to identity/age verification and payment providers only through
adapters. A ``synthetic`` adapter is a local stand-in that performs no real provider
calls and grants nothing on its own — it exists so the foundation runs end-to-end on a
clean checkout without any provider credentials (SAL-007), and so later stories can wire
real providers behind the same interface.

Production rejects synthetic adapters; that rule lives in :mod:`salon.core.config` and is
re-checked here as defence in depth.
"""

from __future__ import annotations

from salon.core.config import SYNTHETIC_ADAPTERS, Settings


def adapter_is_synthetic(name: str) -> bool:
    return name.strip().lower() in SYNTHETIC_ADAPTERS


def assert_adapters_allowed(settings: Settings) -> None:
    """Fail closed if production is somehow configured with a stand-in adapter."""
    if not settings.environment.is_production:
        return
    for label, name in (
        ("verification", settings.verification_adapter),
        ("payment", settings.payment_adapter),
    ):
        if adapter_is_synthetic(name):
            raise RuntimeError(
                f"refusing to start: production {label} adapter is synthetic"
            )
