#!/usr/bin/env python3
"""Independently verify the retained synthetic preflight surfaces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image
import rasterio


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = REPOSITORY_ROOT / "records/synthetic/EXPERIMENT-THREE-SYNTHETIC-PREFLIGHT-2026-001.json"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def roster(root: Path) -> tuple[int, int, str, dict[str, str]]:
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    entries: list[str] = []
    identities: dict[str, str] = {}
    total_bytes = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        size = path.stat().st_size
        digest = file_sha256(path)
        entries.append(f"{relative}\t{size}\t{digest}")
        identities[relative] = digest
        total_bytes += size
    payload = ("\n".join(entries) + "\n").encode("utf-8")
    return len(files), total_bytes, hashlib.sha256(payload).hexdigest(), identities


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
    require(record.get("disposition") == "pass", "preflight disposition is not pass")
    require(record.get("benchmark_accessed") is False, "benchmark boundary changed")
    require(record.get("scientific_output") is False, "synthetic output misclassified")

    for source in record["implementation"]["source_files"]:
        path = REPOSITORY_ROOT / source["path"]
        require(path.is_file(), f"missing source file {source['path']}")
        require(path.stat().st_size == source["bytes"], f"source size drift {source['path']}")
        require(file_sha256(path) == source["sha256"], f"source hash drift {source['path']}")

    observed: dict[str, object] = {}
    identities: list[dict[str, str]] = []
    for role in ("primary_execution", "independent_replay"):
        declared = record[role]
        root = Path(declared["root"])
        require(root.is_dir(), f"missing {role} root")
        count, total_bytes, roster_sha, file_identities = roster(root)
        require(count == declared["files"], f"{role} file-count drift")
        require(total_bytes == declared["bytes"], f"{role} byte-count drift")
        require(roster_sha == declared["roster_sha256"], f"{role} roster drift")
        receipt = root / declared["receipt_path"]
        require(file_sha256(receipt) == declared["receipt_sha256"], f"{role} receipt drift")
        parsed = json.loads(receipt.read_text(encoding="utf-8"))
        require(parsed["benchmark_accessed"] is False, f"{role} benchmark boundary changed")
        require(parsed["scientific_output"] is False, f"{role} scientific boundary changed")
        require(all(parsed["checks"].values()), f"{role} contains a failed check")
        observed[role] = {
            "files": count,
            "bytes": total_bytes,
            "roster_sha256": roster_sha,
            "receipt_sha256": file_sha256(receipt),
            "deterministic_fingerprint": parsed["deterministic_fingerprint"],
        }
        identities.append(file_identities)

    require(identities[0] == identities[1], "primary and replay file bytes differ")
    require(
        observed["primary_execution"]["deterministic_fingerprint"]
        == observed["independent_replay"]["deterministic_fingerprint"],
        "deterministic fingerprints differ",
    )

    primary_root = Path(record["primary_execution"]["root"])
    receipt = json.loads((primary_root / "preflight-receipt.json").read_text(encoding="utf-8"))
    geotiff_path = primary_root / receipt["artifacts"]["geotiff"]["path"]
    with rasterio.open(geotiff_path) as dataset:
        array = dataset.read(1)
        require(dataset.driver == "GTiff", "unexpected GeoTIFF driver")
        require(dataset.crs.to_string() == "EPSG:32610", "GeoTIFF CRS drift")
        require(dataset.tags().get("SURFACE") == "WHOLLY_SYNTHETIC_PREFLIGHT", "synthetic GeoTIFF tag missing")
        require(dataset.tags().get("OPERATIONAL_USE") == "PROHIBITED", "nonoperational tag missing")
        array_hash = hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()
        require(array_hash == receipt["geotiff"]["array_sha256"], "GeoTIFF array drift")

    render_path = primary_root / receipt["artifacts"]["render"]["path"]
    with Image.open(render_path) as image:
        require(image.format == "PNG", "render is not PNG")
        require(image.size == (768, 216), "render dimensions drift")
        colors = image.convert("RGB").getcolors(maxcolors=768 * 216)
        require(colors is not None and len(colors) > 32, "render lacks expected visual variation")

    print(
        json.dumps(
            {
                "status": "pass",
                "record": str(RECORD_PATH),
                "primary": observed["primary_execution"],
                "replay": observed["independent_replay"],
                "geotiff_reopened": True,
                "render_inspected": True,
                "benchmark_accessed": False,
                "scientific_output": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
