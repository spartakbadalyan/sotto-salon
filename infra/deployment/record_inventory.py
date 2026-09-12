"""Record a published candidate; this command never provisions or deploys services."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml
from validate_inventory import validate


def record(
    template: dict, *, digest: str, repository: str, tag: str, commit: str
) -> dict:
    problems = validate(template)
    if problems:
        raise ValueError("invalid inventory template")
    doc = dict(template)
    doc["image"] = {"repository": repository, "digest": digest, "tag": tag}
    doc["config_version"] = commit
    problems = validate(doc, expected_digest=digest)
    if problems:
        raise ValueError("invalid published inventory")
    return doc


def main() -> int:
    try:
        template = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
        doc = record(
            template,
            digest=os.environ["IMAGE_DIGEST"],
            repository=os.environ["IMAGE_REPOSITORY"],
            tag=os.environ["RELEASE_TAG"],
            commit=os.environ["CONFIG_COMMIT"],
        )
        Path(sys.argv[2]).write_text(
            yaml.safe_dump(doc, sort_keys=False), encoding="utf-8"
        )
    except (OSError, ValueError, KeyError, IndexError, yaml.YAMLError):
        print("Cannot record release inventory; inputs redacted", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
