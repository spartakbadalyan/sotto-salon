"""Export the API's OpenAPI schema to a file for contract generation.

Usage: ``python scripts/export_openapi.py ../contracts/openapi/openapi.json``

The export is deterministic (sorted keys, trailing newline) so that regenerating it in
CI is byte-identical when the API is unchanged (SAL-007-AC02).
"""

from __future__ import annotations

import json

# Use synthetic-safe defaults so the schema can be exported without a real environment.
import os
import sys
from pathlib import Path

os.environ.setdefault("SALON_DATABASE_URL", "postgresql+psycopg://salon:salon@127.0.0.1:5432/salon")
os.environ.setdefault("SALON_SESSION_SECRET", "export-only-not-a-secret")

from salon.api.app import create_app  # noqa: E402
from salon.core.config import Settings  # noqa: E402


def build_schema() -> dict:
    app = create_app(Settings())  # type: ignore[call-arg]
    return app.openapi()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: export_openapi.py <output.json>", file=sys.stderr)
        return 2
    out = Path(argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    schema = build_schema()
    out.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
