import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from verify_evidence import verify


class SupplyChainEvidenceTest(unittest.TestCase):
    def fixture(self, root):
        jar = root / "base-repo.jar"
        jar.write_bytes(b"synthetic-jar")
        digest = hashlib.sha256(jar.read_bytes()).hexdigest()
        checksum = root / "SHA256SUMS"
        checksum.write_text(f"{digest}  base-repo.jar\n", encoding="ascii")
        sbom = root / "bom.json"
        sbom.write_text(json.dumps({
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "metadata": {"component": {"type": "application", "name": "base-repo",
                                         "version": "1.0.0", "bom-ref": "root"}},
            "components": [{"type": "library", "name": "dependency", "bom-ref": "dep"}],
            "dependencies": [{"ref": "root", "dependsOn": ["dep"]},
                             {"ref": "dep", "dependsOn": []}],
        }), encoding="utf-8")
        return jar, checksum, sbom

    def test_accepts_consistent_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = verify(*self.fixture(Path(temporary)))
            self.assertTrue(result["valid"])
            self.assertEqual([], result["errors"])

    def test_rejects_modified_jar_and_wrong_component_type(self):
        with tempfile.TemporaryDirectory() as temporary:
            jar, checksum, sbom = self.fixture(Path(temporary))
            jar.write_bytes(b"modified")
            document = json.loads(sbom.read_text())
            document["metadata"]["component"]["type"] = "library"
            sbom.write_text(json.dumps(document), encoding="utf-8")
            result = verify(jar, checksum, sbom)
            self.assertFalse(result["valid"])
            self.assertIn("jar-digest-mismatch", result["errors"])
            self.assertIn("main-component-not-application", result["errors"])


if __name__ == "__main__":
    unittest.main()
