#!/usr/bin/env python3
"""Execute the exact three-seed frozen train/validation lifecycle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from burnlens_experiment_three.data import load_frozen_role  # noqa: E402
from burnlens_experiment_three.protocol import load_protocol  # noqa: E402
from burnlens_experiment_three.training import (  # noqa: E402
    canonical_json,
    reload_seed,
    select_threshold,
    tensor_sha256,
    train_seed,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def roster(root: Path) -> dict[str, object]:
    files = []
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file() and item.name != "exact-replay-receipt.json"
    ):
        files.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    payload = "".join(f"{item['path']}\t{item['bytes']}\t{item['sha256']}\n" for item in files).encode()
    return {"files": files, "file_count": len(files), "total_bytes": sum(item["bytes"] for item in files), "roster_sha256": hashlib.sha256(payload).hexdigest()}


def load_roles(custody_root: Path):
    protocol = load_protocol(ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json")
    return protocol, load_frozen_role(custody_root, protocol, "train"), load_frozen_role(custody_root, protocol, "validation")


def reload_child(args: argparse.Namespace) -> int:
    _, _, validation = load_roles(args.custody_root)
    reload_seed(args.seed, args.package_root, validation, args.result_path)
    return 0


def train_child(args: argparse.Namespace) -> int:
    _, train, validation = load_roles(args.custody_root)
    train_seed(args.seed, train, validation, args.output_root)
    return 0


def read_validation_probabilities(seed_root: Path, patch_ids: tuple[str, ...]) -> torch.Tensor:
    with np.load(seed_root / "validation-probabilities.npz", allow_pickle=False) as archive:
        arrays = [np.asarray(archive[patch_id], dtype=np.float32) for patch_id in patch_ids]
    return torch.from_numpy(np.stack(arrays)[:, None, :, :])


def execute(custody_root: Path, output_root: Path) -> int:
    if output_root.exists():
        raise FileExistsError(output_root)
    output_root.mkdir(parents=True)
    protocol = load_protocol(ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json")
    validation = load_frozen_role(custody_root, protocol, "validation")
    results = {}
    for seed in protocol["execution"]["seeds"]:
        seed_root = output_root / f"seed-{seed}"
        train_command = [
            sys.executable,
            "-I",
            str(Path(__file__).resolve()),
            "--train-child",
            "--custody-root",
            str(custody_root),
            "--output-root",
            str(seed_root),
            "--seed",
            str(seed),
        ]
        trained = subprocess.run(train_command, capture_output=True, text=True, check=False)
        if trained.returncode != 0:
            raise RuntimeError(f"fresh training process failed for seed {seed}: {trained.stderr}")
        manifest = json.loads((seed_root / "run-manifest.json").read_text(encoding="utf-8"))
        reload_path = seed_root / "replay-receipt.json"
        command = [
            sys.executable,
            "-I",
            str(Path(__file__).resolve()),
            "--reload-child",
            "--custody-root",
            str(custody_root),
            "--package-root",
            str(seed_root / "selected-checkpoint"),
            "--seed",
            str(seed),
            "--result-path",
            str(reload_path),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"fresh reload failed for seed {seed}: {completed.stderr}")
        reloaded = json.loads(reload_path.read_text(encoding="utf-8"))
        if reloaded["tensor_state_sha256"] != manifest["checkpoint_tensor_state_sha256"]:
            raise RuntimeError("fresh reload tensor hash mismatch")
        probabilities = read_validation_probabilities(seed_root, validation.patch_ids)
        if reloaded["probabilities_sha256"] != tensor_sha256(probabilities):
            raise RuntimeError("fresh reload probability mismatch")
        if reloaded["validation_balanced_bce"] != manifest["selected_validation_balanced_bce"]:
            raise RuntimeError("fresh reload validation loss mismatch")
        results[seed] = {"probabilities": probabilities}
    threshold = select_threshold(results, validation)
    canonical_json(output_root / "shared-threshold-selection.json", threshold)
    summary = {
        "schema_version": "1.0",
        "run_id": "EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001",
        "status": "pass",
        "protocol_id": protocol["protocol_id"],
        "seeds": protocol["execution"]["seeds"],
        "selected_threshold": threshold["selected_threshold"],
        "test_arrays_listed_or_decoded": 0,
        "test_values_opened": False,
        "training_runs": 3,
        "checkpoints": 3,
        "inference_scope": "validation_only",
        "evaluation_runs": 0,
        "roster": roster(output_root),
    }
    canonical_json(output_root / "exact-replay-receipt.json", summary)
    print(json.dumps({"status": "PASS", "output": str(output_root), "selected_threshold": threshold["selected_threshold"], "roster_sha256": summary["roster"]["roster_sha256"], "test_values_opened": False}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--custody-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--reload-child", action="store_true")
    parser.add_argument("--train-child", action="store_true")
    parser.add_argument("--package-root", type=Path)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--result-path", type=Path)
    args = parser.parse_args()
    if args.reload_child:
        if args.package_root is None or args.result_path is None or args.seed is None:
            parser.error("reload child requires seed, package, and result paths")
        return reload_child(args)
    if args.train_child:
        if args.output_root is None or args.seed is None:
            parser.error("train child requires seed and output root")
        return train_child(args)
    if args.output_root is None:
        parser.error("output root is required")
    return execute(args.custody_root, args.output_root)


if __name__ == "__main__":
    raise SystemExit(main())
