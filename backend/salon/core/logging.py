"""Minimal structured logging setup.

Telemetry must never carry ad text, identity documents, contact details, credentials,
or raw provider payloads (see the architecture's operations section). This module only
configures formatting; scrubbing rules land with observability in SAL-025.
"""

from __future__ import annotations

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
