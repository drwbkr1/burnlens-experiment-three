#!/usr/bin/env python3
"""Verify an extracted Experiment Three public evidence package."""

from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path


FORBIDDEN_SUFFIXES = {".npy", ".npz", ".pt", ".pth", ".tif", ".tiff"}
EXPECTED_PACKAGE_ID = "BURNLENS-EXPERIMENT-THREE-v1.0.0-EVIDENCE"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(package_root: Path, manifest_path: Path | None = None) -> dict[str, object]:
    manifest_path = manifest_path or package_root / "release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package_id") != EXPECTED_PACKAGE_ID or manifest.get("version") != "1.0.0" or manifest.get("expected_tag") != "v1.0.0":
        raise ValueError("release package identity changed")
    if manifest.get("dispositions") != {"lifecycle_status": "PASS", "comparative_status": "FAIL"}:
        raise ValueError("release dispositions changed")
    if manifest.get("rights_boundary", {}).get("forbidden_bytes_included") != 0:
        raise ValueError("release rights boundary changed")
    expected = {item["path"]: item for item in manifest.get("files", [])}
    actual_paths = sorted(
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*")
        if path.is_file() and path.resolve() != manifest_path.resolve()
    )
    if actual_paths != sorted(expected):
        raise ValueError("release package file roster changed")
    total_bytes = 0
    for relative, identity in expected.items():
        path = package_root / relative
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            raise ValueError(f"forbidden release file: {relative}")
        if path.stat().st_size != identity["bytes"] or sha256(path) != identity["sha256"]:
            raise ValueError(f"release file identity mismatch: {relative}")
        total_bytes += path.stat().st_size
    result = json.loads((package_root / "evidence/evaluation-record.json").read_text(encoding="utf-8"))
    if result.get("dispositions", {}).get("lifecycle_status") != "PASS" or result.get("dispositions", {}).get("comparative_status") != "FAIL" or result.get("opening", {}).get("post_test_changes") != 0:
        raise ValueError("packaged evaluation outcome changed")
    public_manifest = json.loads((package_root / "evidence/public-evidence-manifest.json").read_text(encoding="utf-8"))
    if public_manifest.get("forbidden_bytes_included") != 0 or public_manifest.get("dispositions") != {"comparative_status": "FAIL", "lifecycle_status": "PASS"}:
        raise ValueError("packaged public evidence boundary changed")
    svg_count = 0
    for path in sorted((package_root / "figures").glob("*.svg")):
        text = path.read_text(encoding="utf-8")
        ET.fromstring(text)
        lowered = text.lower()
        if "<image" in lowered or "base64" in lowered or "data:" in lowered:
            raise ValueError(f"embedded byte surface in {path.name}")
        svg_count += 1
    if svg_count != 3:
        raise ValueError("expected three numerical SVGs")
    return {
        "status": "PASS",
        "package_id": EXPECTED_PACKAGE_ID,
        "files": len(expected),
        "bytes": total_bytes,
        "manifest_sha256": sha256(manifest_path),
        "svg_xml_parsed": svg_count,
        "forbidden_files": 0,
        "lifecycle_status": "PASS",
        "comparative_status": "FAIL",
        "post_test_changes": 0,
        "scope": manifest["verification_scope"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.package_root, args.manifest), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
