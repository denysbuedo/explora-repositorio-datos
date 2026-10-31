import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from audit_repository import audit


class OcflAuditTest(unittest.TestCase):
    def object(self, root, name, algorithm="sha256", corrupt=False):
        directory = root / name
        directory.mkdir()
        inventory = {
            "id": f"urn:test:{name}",
            "type": "https://ocfl.io/1.1/spec/#inventory",
            "digestAlgorithm": algorithm,
            "head": "v1",
            "manifest": {},
            "versions": {},
        }
        raw = json.dumps(inventory, separators=(",", ":")).encode()
        (directory / "inventory.json").write_bytes(raw)
        digest = hashlib.new(algorithm, raw).hexdigest()
        if corrupt:
            digest = "0" * len(digest)
        (directory / f"inventory.json.{algorithm}").write_text(
            f"{digest} inventory.json\n", encoding="ascii"
        )

    def test_classifies_historical_md5_and_new_sha256_without_rewriting(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.object(root, "legacy", "md5")
            self.object(root, "current", "sha256")
            report = audit(root)
            self.assertEqual({"md5": 1, "sha256": 1}, report["algorithms"])
            self.assertEqual(2, report["valid"])
            self.assertEqual(0, report["invalid"])

    def test_reports_mismatch_and_duplicate_object_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.object(root, "one", corrupt=True)
            self.object(root, "two")
            inventory_path = root / "two" / "inventory.json"
            inventory = json.loads(inventory_path.read_text())
            inventory["id"] = "urn:test:one"
            raw = json.dumps(inventory, separators=(",", ":")).encode()
            inventory_path.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            (root / "two" / "inventory.json.sha256").write_text(
                f"{digest} inventory.json\n", encoding="ascii"
            )
            report = audit(root)
            self.assertEqual(1, report["invalid"])
            self.assertEqual(["urn:test:one"], report["duplicateIds"])


if __name__ == "__main__":
    unittest.main()
