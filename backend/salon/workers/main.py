"""Worker entrypoint.

A separate process from the API, per the architecture. It shares configuration and the
production adapter guard. Job handling (outbox draining, media, retention, billing
reconciliation) arrives in later stories; this foundation only proves the process boots
with the same safety checks as the API.
"""

from __future__ import annotations

import logging

from salon.core.adapters import assert_adapters_allowed
from salon.core.config import get_settings
from salon.core.logging import configure_logging

log = logging.getLogger("salon.worker")


def main() -> None:
    configure_logging()
    settings = get_settings()
    assert_adapters_allowed(settings)
    log.info("worker starting in %s environment", settings.environment.value)
    # No queue loop yet (SAL-008/SAL-009+). Exit cleanly so the entrypoint is testable.


if __name__ == "__main__":
    main()
