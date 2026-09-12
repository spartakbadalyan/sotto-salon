"""Validate deployment records without printing potentially secret input values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

SCHEMA = json.loads(Path(__file__).with_name("inventory.schema.json").read_text())


def validate(doc: Any, *, expected_digest: str | None = None) -> list[str]:
    problems = []
    for error in Draft202012Validator(SCHEMA).iter_errors(doc):
        # Neither values nor caller-supplied property names are safe to log.
        problems.append(f"inventory violates schema rule: {error.validator}")
    if problems:
        return problems
    if doc["provisioning"] == "live" and doc["image"]["digest"] == "sha256:" + "0" * 64:
        problems.append("live inventory cannot use the synthetic placeholder digest")
    if expected_digest is not None and doc["image"]["digest"] != expected_digest:
        problems.append("inventory digest does not match the published image")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--expected-digest")
    args = parser.parse_args()
    try:
        doc = yaml.safe_load(args.inventory.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        print("Cannot read or parse inventory; input contents redacted")
        return 2
    problems = validate(doc, expected_digest=args.expected_digest)
    if problems:
        print("\n".join(problems))
        return 1
    print("OK: inventory schema and digest checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
