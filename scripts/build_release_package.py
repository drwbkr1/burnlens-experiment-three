#!/usr/bin/env python3
"""Build the deterministic, rights-safe Experiment Three public evidence ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "burnlens-experiment-three-v1.0.0-evidence"
ARCHIVE_NAME = f"{PACKAGE_NAME}.zip"
MANIFEST_NAME = "release-manifest.json"
FIXED_TIME = (2026, 8, 25, 0, 0, 0)
PACKAGE_MAP = (
    (Path("docs/release/RELEASE-NOTES-v1.0.0.md"), Path("README.md")),
    (Path("docs/evidence/REVIEWER-GUIDE.md"), Path("REVIEWER-GUIDE.md")),
    (Path("docs/benchmark/BENCHMARK-CARD.md"), Path("BENCHMARK-CARD.md")),
    (Path("docs/model-card/MODEL-CARD.md"), Path("MODEL-CARD.md")),
    (Path("docs/limitations/LIMITATIONS.md"), Path("LIMITATIONS.md")),
    (Path("docs/reproducibility/REPRODUCIBILITY.md"), Path("REPRODUCIBILITY.md")),
    (Path("docs/evidence/generated/architecture.svg"), Path("figures/architecture.svg")),
    (Path("docs/evidence/generated/training-curves.svg"), Path("figures/training-curves.svg")),
    (Path("docs/evidence/generated/comparative-summary.svg"), Path("figures/comparative-summary.svg")),
    (Path("records/evaluation/EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json"), Path("evidence/evaluation-record.json")),
    (Path("records/release/EXPERIMENT-THREE-PUBLIC-EVIDENCE-MANIFEST-2026-001.json"), Path("evidence/public-evidence-manifest.json")),
    (Path("protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"), Path("evidence/frozen-protocol.json")),
    (Path("scripts/verify_release_package.py"), Path("verify_release_package.py")),
    (Path("LICENSE"), Path("LICENSE")),
)
FORBIDDEN_SUFFIXES = {".npy", ".npz", ".pt", ".pth", ".tif", ".tiff"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def zip_directory(package_root: Path, archive: Path) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(package_root.rglob("*"), key=lambda item: item.relative_to(package_root).as_posix()):
            if not path.is_file():
                continue
            relative = path.relative_to(package_root).as_posix()
            info = zipfile.ZipInfo(f"{PACKAGE_NAME}/{relative}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    package_root = output_dir / PACKAGE_NAME
    archive = output_dir / ARCHIVE_NAME
    checksum = output_dir / f"{ARCHIVE_NAME}.sha256"
    for path in (package_root, archive, checksum):
        if path.exists():
            raise FileExistsError(f"refusing to replace existing release output: {path}")
    package_root.mkdir()
    files = []
    for source_relative, destination_relative in PACKAGE_MAP:
        if source_relative.suffix.lower() in FORBIDDEN_SUFFIXES or destination_relative.suffix.lower() in FORBIDDEN_SUFFIXES:
            raise ValueError(f"forbidden release suffix: {source_relative}")
        source = ROOT / source_relative
        destination = package_root / destination_relative
        if not source.is_file():
            raise FileNotFoundError(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        destination.write_bytes(data)
        files.append({"path": destination_relative.as_posix(), "bytes": len(data), "sha256": sha256_bytes(data), "source": source_relative.as_posix()})
    manifest = {
        "schema_version": "burnlens-exp3-release-package/v1",
        "package_id": "BURNLENS-EXPERIMENT-THREE-v1.0.0-EVIDENCE",
        "version": "1.0.0",
        "expected_tag": "v1.0.0",
        "source_checkpoint": {"commit": "45b32c1cb782edc31ef8a4f49671b6a897c7d7bb", "tree": "91fb304d4cadc450ed997c0d3f68c995b5538cb4"},
        "dispositions": {"lifecycle_status": "PASS", "comparative_status": "FAIL"},
        "verification_scope": "standalone public-package byte and evidence consistency; not public-download scientific inference replay",
        "files": sorted(files, key=lambda item: item["path"]),
        "rights_boundary": {"forbidden_bytes_included": 0, "controlled_only": ["benchmark arrays", "source imagery", "labels", "historical comparator arrays", "model checkpoints", "predictions", "probabilities", "GeoTIFFs", "imagery-bearing comparison render", "runtime", "private review material"]},
    }
    manifest_bytes = canonical_json(manifest)
    (package_root / MANIFEST_NAME).write_bytes(manifest_bytes)
    zip_directory(package_root, archive)
    archive_sha = sha256_bytes(archive.read_bytes())
    checksum.write_text(f"{archive_sha}  {ARCHIVE_NAME}\n", encoding="ascii", newline="\n")
    return {
        "status": "PASS",
        "package_root": str(package_root),
        "payload_files": len(files),
        "payload_bytes": sum(item["bytes"] for item in files),
        "manifest_bytes": len(manifest_bytes),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "archive": str(archive),
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": archive_sha,
        "checksum_sha256": sha256_bytes(checksum.read_bytes()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
