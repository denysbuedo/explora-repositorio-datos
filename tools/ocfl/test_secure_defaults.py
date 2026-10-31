import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def properties(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        separator = ":" if ":" in line else "="
        key, value = line.split(separator, 1)
        values[key.strip()] = value.strip().strip('"')
    return values


class SecureDefaultsTest(unittest.TestCase):
    def test_ocfl_new_object_digest_is_sha256_while_plugin_remains_disabled(self):
        config = properties(ROOT / "config" / "application-default.properties")
        self.assertEqual("sha256", config["ocfl.hashing.digest.algorithm"])
        self.assertEqual("simple", config["repo.plugin.versioning"])

    def test_only_modern_tls_protocols_are_enabled(self):
        config = properties(ROOT / "gradle.properties")
        self.assertEqual("TLSv1.2,TLSv1.3", config["systemProp.jdk.tls.client.protocols"])


if __name__ == "__main__":
    unittest.main()
