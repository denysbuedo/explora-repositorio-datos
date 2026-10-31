import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT / "src/main/resources/application-production.properties"
MIGRATION = ROOT / "src/main/resources/db/migration/postgresql/V1__scientific_repository_extension.sql"


def properties(path):
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            result[key] = value
    return result


class FlywayConfigurationTest(unittest.TestCase):
    def test_production_uses_validate_and_safe_flyway_settings(self):
        config = properties(PRODUCTION)
        self.assertEqual("validate", config["spring.jpa.hibernate.ddl-auto"])
        self.assertEqual("true", config["spring.flyway.enabled"])
        self.assertEqual("true", config["spring.flyway.clean-disabled"])
        self.assertEqual("false", config["spring.flyway.baseline-on-migrate"])
        self.assertEqual("0", config["spring.flyway.baseline-version"])
        self.assertEqual("false", config["spring.flyway.out-of-order"])

    def test_non_production_profiles_do_not_run_postgresql_migrations(self):
        for relative in (
            "config/application-default.properties",
            "config/application-docker.properties",
            "src/test/resources/test-config/application-test.properties",
            "src/test/resources/test-config/application-doc.properties",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^spring\.flyway\.enabled\s*[:=]\s*false$")

    def test_versioned_migration_has_no_manual_transaction_or_destructive_ddl(self):
        sql = MIGRATION.read_text(encoding="utf-8")
        self.assertNotRegex(sql, r"(?im)^\s*(BEGIN|COMMIT)\s*;")
        self.assertNotRegex(sql, r"(?i)\b(DROP|TRUNCATE)\b")
        self.assertRegex(sql, r"(?i)CREATE TABLE IF NOT EXISTS scientific_records")
        self.assertRegex(sql, r"(?i)ALTER TABLE repo_users ADD COLUMN IF NOT EXISTS")

    def test_only_one_version_uses_each_number(self):
        migrations = list(MIGRATION.parent.glob("V*__*.sql"))
        versions = [re.match(r"V([^_]+)__", path.name).group(1) for path in migrations]
        self.assertEqual(len(versions), len(set(versions)))


if __name__ == "__main__":
    unittest.main()
