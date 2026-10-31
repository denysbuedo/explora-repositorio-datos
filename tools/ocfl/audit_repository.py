#!/usr/bin/env python3
"""Audita inventarios OCFL sin modificar el repositorio."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

SUPPORTED = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
    "blake2b-512": lambda data=b"": hashlib.blake2b(data, digest_size=64),
}
SIDECAR = re.compile(r"^([0-9a-fA-F]+)[ \t]+inventory\.json\s*$")


def inventory_paths(root: Path):
    for directory, names, files in os.walk(root, followlinks=False):
        names[:] = [name for name in names if not (Path(directory) / name).is_symlink()]
        if "inventory.json" in files:
            yield Path(directory) / "inventory.json"


def audit_inventory(path: Path, root: Path) -> dict:
    relative = path.relative_to(root).as_posix()
    result = {"path": relative, "valid": False, "algorithm": None, "id": None, "errors": []}
    try:
        raw = path.read_bytes()
        inventory = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        result["errors"].append(f"inventory-unreadable:{type(error).__name__}")
        return result

    if not isinstance(inventory, dict):
        result["errors"].append("inventory-not-object")
        return result

    result["id"] = inventory.get("id")
    algorithm = inventory.get("digestAlgorithm")
    result["algorithm"] = algorithm
    if not isinstance(result["id"], str) or not result["id"].strip():
        result["errors"].append("missing-id")
    if algorithm not in SUPPORTED:
        result["errors"].append("unsupported-digest-algorithm")
        return result
    if not isinstance(inventory.get("manifest"), dict):
        result["errors"].append("missing-manifest")
    if not isinstance(inventory.get("versions"), dict):
        result["errors"].append("missing-versions")

    sidecar = path.with_name(f"inventory.json.{algorithm}")
    try:
        sidecar_text = sidecar.read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError) as error:
        result["errors"].append(f"sidecar-unreadable:{type(error).__name__}")
        return result
    match = SIDECAR.fullmatch(sidecar_text)
    if not match:
        result["errors"].append("invalid-sidecar-format")
        return result
    actual = SUPPORTED[algorithm](raw).hexdigest()
    if match.group(1).lower() != actual:
        result["errors"].append("inventory-digest-mismatch")
    result["valid"] = not result["errors"]
    return result


def audit(root: Path) -> dict:
    resolved = root.resolve(strict=True)
    if not resolved.is_dir():
        raise NotADirectoryError(resolved)
    objects = [audit_inventory(path, resolved) for path in inventory_paths(resolved)]
    identifiers = Counter(item["id"] for item in objects if item["id"])
    duplicates = sorted(identifier for identifier, count in identifiers.items() if count > 1)
    algorithms = Counter(item["algorithm"] or "unknown" for item in objects)
    invalid = sum(not item["valid"] for item in objects)
    return {
        "root": str(resolved),
        "objects": len(objects),
        "valid": len(objects) - invalid,
        "invalid": invalid,
        "algorithms": dict(sorted(algorithms.items())),
        "duplicateIds": duplicates,
        "results": objects,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="copia montada en solo lectura del storage root OCFL")
    parser.add_argument("--summary-only", action="store_true", help="omite el detalle por objeto")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root)
    except (OSError, NotADirectoryError) as error:
        print(json.dumps({"error": type(error).__name__, "message": str(error)}, ensure_ascii=False))
        return 2
    if args.summary_only:
        report.pop("results")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if report["invalid"] or report["duplicateIds"] else 0


if __name__ == "__main__":
    sys.exit(main())
