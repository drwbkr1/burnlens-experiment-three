#!/usr/bin/env python3
"""Verify M5 input identities without deserializing test or comparator arrays."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "records/intake/EXPERIMENT-ONE-BENCHMARK-ADMISSION-MANIFEST-2026-001.json"
RECEIPT = ROOT / "records/intake/EXPERIMENT-ONE-BENCHMARK-INTAKE-RECEIPT-2026-001.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def category(relative: str) -> str | None:
    if "/patches/test--" in relative and relative.endswith(".npy"):
        return "test_dataset_arrays"
    if "/bounded-unet-test-v0.1.0/predictions/" in relative and relative.endswith(".npy"):
        return "unet_test_arrays"
    if relative.endswith("/BASELINE-EVALUATION-2026-001.json"):
        return "rbr_comparator_record"
    if relative.endswith("/BOUNDED-UNET-TEST-EVALUATION-2026-001.json"):
        return "unet_comparator_record"
    if relative.endswith(("/DATASET-MANIFEST.json", "/WHOLE-EVENT-SPLIT-2026-001.json", "/TRAIN-NORMALIZATION-2026-001.json")):
        return "binding_record"
    return None


def verify(custody_root: Path, evaluation_root: Path) -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    receipt_by_id = {asset["asset_id"]: asset for asset in receipt["assets"]}
    groups: dict[str, dict[str, object]] = {}
    for asset in manifest["assets"]:
        relative = asset["destination_relative_path"]
        group_name = category(relative)
        if group_name is None:
            continue
        target = custody_root / Path(relative)
        promoted = receipt_by_id[asset["asset_id"]]["observed"]
        size = target.stat().st_size
        digest = sha256(target)
        if size != asset["expected"]["size_bytes"] or size != promoted["promoted_size_bytes"]:
            raise RuntimeError(f"size mismatch: {asset['asset_id']}")
        if digest != asset["expected"]["sha256"] or digest != promoted["promoted_sha256"]:
            raise RuntimeError(f"SHA-256 mismatch: {asset['asset_id']}")
        group = groups.setdefault(group_name, {"files": 0, "bytes": 0, "roster": []})
        group["files"] = int(group["files"]) + 1
        group["bytes"] = int(group["bytes"]) + size
        group["roster"].append(f"{relative}\t{size}\t{digest}")
    for group in groups.values():
        roster = "\n".join(sorted(group.pop("roster"))) + "\n"
        group["roster_sha256"] = hashlib.sha256(roster.encode("utf-8")).hexdigest()
        group["mismatches"] = 0
    expected = {
        "binding_record": (3, 70314, "19973be5c98d1c7a246dfbd4e89af1018b95e89b008a5d9857ffe92807ff4839"),
        "rbr_comparator_record": (1, 21257, "05ceda96f8d756f5b6d9d8b11e2a41ccb8923868814c436cd210d7c9f5b3ffbb"),
        "test_dataset_arrays": (16, 444416, "04061c6a6747421e2cb4afbc079f2611c22ec6944c0839391c2b6a1611275321"),
        "unet_comparator_record": (1, 26268, "449cf35b0c51ed43dc3d2adae6dc9b35758880c8625d8d68c415d5b2736fee6a"),
        "unet_test_arrays": (8, 82944, "1c6bbd067273a5b1526aac0bfd7f43a92db36ef9259632da1b46840b5b0467d1"),
    }
    for name, (files, byte_count, roster_hash) in expected.items():
        observed = groups.get(name, {})
        if (observed.get("files"), observed.get("bytes"), observed.get("roster_sha256")) != (files, byte_count, roster_hash):
            raise RuntimeError(f"pre-opening roster mismatch: {name}")
    if evaluation_root.exists():
        raise RuntimeError("M5 evaluation root already exists; opening state is not sealed")
    return {
        "status": "PASS",
        "operation": "cryptographic hashing and JSON metadata validation only",
        "groups": groups,
        "arrays_deserialized": 0,
        "values_decoded": 0,
        "numpy_imported": False,
        "evaluation_root_absent": True,
        "opening_marker_exists": False,
        "terminal_package_exists": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--custody-root", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.custody_root, args.evaluation_root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
