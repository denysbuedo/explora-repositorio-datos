#!/usr/bin/env python3
"""Verifica que JAR, SHA256SUMS y SBOM CycloneDX describan el mismo candidato."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

CHECKSUM = re.compile(r"^([0-9a-fA-F]{64}) [ *](\S+)$")


def verify(jar: Path, checksum_file: Path, sbom_file: Path) -> dict:
    errors = []
    jar_bytes = jar.read_bytes()
    actual_digest = hashlib.sha256(jar_bytes).hexdigest()
    lines = [line for line in checksum_file.read_text(encoding="ascii").splitlines() if line]
    match = CHECKSUM.fullmatch(lines[0]) if len(lines) == 1 else None
    if not match:
        errors.append("invalid-checksum-file")
    else:
        if Path(match.group(2)).name != jar.name:
            errors.append("checksum-filename-mismatch")
        if match.group(1).lower() != actual_digest:
            errors.append("jar-digest-mismatch")

    sbom = json.loads(sbom_file.read_text(encoding="utf-8"))
    metadata = sbom.get("metadata") if isinstance(sbom, dict) else None
    component = metadata.get("component") if isinstance(metadata, dict) else None
    components = sbom.get("components") if isinstance(sbom, dict) else None
    dependencies = sbom.get("dependencies") if isinstance(sbom, dict) else None
    if sbom.get("bomFormat") != "CycloneDX":
        errors.append("invalid-bom-format")
    if not isinstance(component, dict) or component.get("type") != "application":
        errors.append("main-component-not-application")
    version = component.get("version") if isinstance(component, dict) else None
    if not isinstance(version, str) or not version.strip() or version == "unspecified":
        errors.append("invalid-component-version")
    if not isinstance(components, list) or not components:
        errors.append("missing-components")
        components = []
    if not isinstance(dependencies, list) or not dependencies:
        errors.append("missing-dependency-graph")
        dependencies = []
    component_refs = [item.get("bom-ref") for item in components if isinstance(item, dict)]
    if None in component_refs or len(component_refs) != len(set(component_refs)):
        errors.append("invalid-component-references")
    known_refs = set(component_refs)
    if isinstance(component, dict) and component.get("bom-ref"):
        known_refs.add(component["bom-ref"])
    dependency_refs = {item.get("ref") for item in dependencies if isinstance(item, dict)}
    if None in dependency_refs or not dependency_refs.issubset(known_refs):
        errors.append("unknown-dependency-reference")
    return {
        "valid": not errors,
        "errors": errors,
        "sha256": actual_digest,
        "component": component.get("name") if isinstance(component, dict) else None,
        "version": version,
        "components": len(components),
        "dependencies": len(dependencies),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jar", type=Path)
    parser.add_argument("checksum", type=Path)
    parser.add_argument("sbom", type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify(args.jar, args.checksum, args.sbom)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        result = {"valid": False, "errors": [f"unreadable-evidence:{type(error).__name__}"]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
