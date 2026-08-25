#!/usr/bin/env python3
"""Independently verify M4 frozen training, reload, threshold, and replay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import torch  # noqa: E402

from burnlens_experiment_three.checkpoint import load_state_dict_package  # noqa: E402
from burnlens_experiment_three.data import load_frozen_role  # noqa: E402
from burnlens_experiment_three.model import FixedBurnChangeDetector  # noqa: E402
from burnlens_experiment_three.protocol import load_protocol  # noqa: E402
from burnlens_experiment_three.selection import EpochObservation, early_stop_epoch, select_checkpoint  # noqa: E402
from burnlens_experiment_three.training import configure, evaluate_loss, select_threshold, tensor_sha256  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path) -> dict[str, tuple[int, str]]:
    return {path.relative_to(root).as_posix(): (path.stat().st_size, sha(path)) for path in root.rglob("*") if path.is_file()}


def verify(primary: Path, replay: Path, custody: Path) -> dict[str, object]:
    primary_files = files(primary)
    replay_files = files(replay)
    if primary_files != replay_files:
        raise RuntimeError("primary and replay bytes differ")
    receipt = json.loads(
        (primary / "exact-replay-receipt.json").read_text(encoding="utf-8")
    )
    if receipt["test_values_opened"] is not False or receipt["test_arrays_listed_or_decoded"] != 0:
        raise RuntimeError("test boundary violated")
    if receipt["training_runs"] != 3 or receipt["checkpoints"] != 3:
        raise RuntimeError("run/checkpoint count drift")
    expected_roster = {item["path"]: (item["bytes"], item["sha256"]) for item in receipt["roster"]["files"]}
    actual_without_receipt = {
        name: value
        for name, value in primary_files.items()
        if name != "exact-replay-receipt.json"
    }
    if expected_roster != actual_without_receipt:
        raise RuntimeError("receipt roster mismatch")

    protocol = load_protocol(ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json")
    validation = load_frozen_role(custody, protocol, "validation")
    results = {}
    seeds_summary = []
    for seed in protocol["execution"]["seeds"]:
        seed_root = primary / f"seed-{seed}"
        expected_artifacts = set(protocol["artifacts"]["per_seed"])
        observed_artifacts = {
            path.relative_to(seed_root).as_posix()
            for path in seed_root.rglob("*")
            if path.is_file()
        }
        if observed_artifacts != expected_artifacts:
            raise RuntimeError(f"frozen per-seed artifact roster drift for {seed}")
        run_manifest = json.loads(
            (seed_root / "run-manifest.json").read_text(encoding="utf-8")
        )
        runtime = run_manifest.get("runtime", {})
        if run_manifest.get("process_scope") != "fresh_isolated_subprocess_per_seed" or run_manifest.get(
            "exception"
        ) is not None or run_manifest.get("test_values_opened") is not False:
            raise RuntimeError(f"process, exception, or test boundary drift for {seed}")
        if runtime != {
            "python": "3.12.10",
            "torch": "2.13.0+cpu",
            "device": "cpu",
            "dtype": "float32",
            "num_threads": 1,
            "num_interop_threads": 1,
        }:
            raise RuntimeError(f"runtime identity drift for {seed}")
        history = json.loads((seed_root / "training-history.json").read_text(encoding="utf-8"))
        observations = [EpochObservation(row["epoch"], row["validation_balanced_bce"]) for row in history["rows"]]
        selected = select_checkpoint(observations)
        if selected.epoch != history["selected_epoch"] or selected.validation_loss != history["selected_validation_balanced_bce"]:
            raise RuntimeError(f"checkpoint selection drift for {seed}")
        if early_stop_epoch(observations) != history["epochs_completed"]:
            raise RuntimeError(f"early-stop drift for {seed}")
        if not (history["first_gradient_norm"] > 0.0 and history["initial_tensor_state_sha256"] != history["first_step_tensor_state_sha256"]):
            raise RuntimeError(f"gradient or weight-change gate failed for {seed}")
        configure(seed)
        model = FixedBurnChangeDetector()
        package = load_state_dict_package(model, seed_root / "selected-checkpoint")
        loss, probabilities = evaluate_loss(model, validation)
        reload = json.loads((seed_root / "replay-receipt.json").read_text(encoding="utf-8"))
        if package["tensor_state_sha256"] != reload["tensor_state_sha256"] or loss != reload["validation_balanced_bce"] or tensor_sha256(probabilities) != reload["probabilities_sha256"]:
            raise RuntimeError(f"fresh reload drift for {seed}")
        with np.load(seed_root / "validation-probabilities.npz", allow_pickle=False) as archive:
            for index, patch_id in enumerate(validation.patch_ids):
                if not np.array_equal(archive[patch_id], probabilities[index, 0].numpy()):
                    raise RuntimeError(f"probability package drift for {seed}/{patch_id}")
        results[seed] = {"probabilities": probabilities}
        seeds_summary.append({"seed": seed, "epochs": history["epochs_completed"], "selected_epoch": selected.epoch, "validation_balanced_bce": selected.validation_loss, "tensor_state_sha256": package["tensor_state_sha256"]})
    expected_threshold = select_threshold(results, validation)
    observed_threshold = json.loads((primary / "shared-threshold-selection.json").read_text(encoding="utf-8"))
    if expected_threshold != observed_threshold or observed_threshold["selected_threshold"] != 0.5:
        raise RuntimeError("shared threshold replay drift")
    return {"status": "PASS", "files": len(primary_files), "bytes": sum(value[0] for value in primary_files.values()), "roster_sha256": receipt["roster"]["roster_sha256"], "selected_threshold": 0.5, "seeds": seeds_summary, "primary_replay_exact": True, "test_values_opened": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--custody-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.primary, args.replay, args.custody_root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
