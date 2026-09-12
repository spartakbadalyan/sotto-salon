import copy
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from record_inventory import record
from validate_inventory import validate


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.doc = yaml.safe_load(
            (Path(__file__).resolve().parents[1] / "staging.inventory.yaml").read_text(
                encoding="utf-8"
            )
        )

    def test_synthetic_template(self):
        self.assertEqual(validate(self.doc), [])

    def test_unknown_fields_are_rejected_at_every_level(self):
        for target in (self.doc, self.doc["image"], self.doc["secret_references"][0]):
            target["password"] = "synthetic-plaintext"
            problems = validate(self.doc)
            self.assertTrue(problems)
            self.assertNotIn("synthetic-plaintext", str(problems))
            del target["password"]

    def test_invalid_types_and_provisioning(self):
        for key, value in [
            ("environment", []),
            ("provisioning", "invalid"),
            ("secret_references", {}),
            ("config_version", 123),
        ]:
            doc = copy.deepcopy(self.doc)
            doc[key] = value
            self.assertTrue(validate(doc))
        self.doc["image"]["repository"] = 123
        self.assertTrue(validate(self.doc))

    def test_live_placeholder_rejected(self):
        self.doc["provisioning"] = "live"
        self.assertTrue(validate(self.doc))

    def test_digest_mismatch_rejected(self):
        self.assertTrue(validate(self.doc, expected_digest="sha256:" + "a" * 64))

    def test_record_binds_actual_image_and_config(self):
        digest = "sha256:" + "a" * 64
        doc = record(
            self.doc,
            digest=digest,
            repository="ghcr.io/example/api",
            tag="v1.0.0",
            commit="abc123",
        )
        self.assertEqual(validate(doc, expected_digest=digest), [])
        self.assertEqual(doc["config_version"], "abc123")
        self.assertEqual(doc["secret_references"], self.doc["secret_references"])
        self.assertNotEqual(self.doc["image"]["digest"], digest)

    def test_record_refuses_invalid_template_and_digest(self):
        for digest in ("latest", ""):
            with self.assertRaises(ValueError):
                record(
                    self.doc,
                    digest=digest,
                    repository="ghcr.io/example/api",
                    tag="v1.0.0",
                    commit="abc123",
                )
        self.doc["password"] = "synthetic-plaintext"
        with self.assertRaises(ValueError):
            record(
                self.doc,
                digest="sha256:" + "a" * 64,
                repository="ghcr.io/example/api",
                tag="v1.0.0",
                commit="abc123",
            )
