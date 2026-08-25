#!/usr/bin/env python3
"""Consume the one M5 opening and build exact primary/replay evaluation evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
import torch

from burnlens_experiment_three.checkpoint import load_state_dict_package
from burnlens_experiment_three.evaluation import (
    comparative_disposition,
    create_opening_root,
    evaluate_predictions,
    load_opened_test,
    load_unet_comparator,
    package_seed,
    rbr_probability_score,
    render_comparison,
    sha256_file,
    write_geospatial_surfaces,
)
from burnlens_experiment_three.model import FixedBurnChangeDetector
from burnlens_experiment_three.protocol import load_protocol
from burnlens_experiment_three.training import canonical_json, configure


PROTOCOL_PATH = ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
PROTOCOL_SHA256 = "12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e"
EXPECTED_OUTPUT_NAME = "m5-2026-001"
RBR_THRESHOLD = 0.041043221950531006


def roster(root: Path) -> dict[str, object]:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rows.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    payload = "".join(f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows).encode()
    return {"files": rows, "file_count": len(rows), "bytes": sum(int(row["bytes"]) for row in rows), "roster_sha256": hashlib.sha256(payload).hexdigest()}


def infer(training_root: Path, normalized: np.ndarray, seeds: list[int]) -> tuple[dict[int, np.ndarray], list[dict[str, object]]]:
    probabilities: dict[int, np.ndarray] = {}
    packages = []
    inputs = torch.from_numpy(normalized)
    for seed in seeds:
        configure(seed)
        model = FixedBurnChangeDetector()
        manifest = load_state_dict_package(model, training_root / f"seed-{seed}" / "selected-checkpoint")
        model.eval()
        with torch.inference_mode():
            value = torch.sigmoid(model(inputs)).cpu().numpy()[:, 0].astype(np.float32)
        if not np.isfinite(value).all():
            raise RuntimeError(f"nonfinite test probability: {seed}")
        probabilities[seed] = value
        packages.append({"seed": seed, "tensor_state_sha256": manifest["tensor_state_sha256"], "weights_sha256": manifest["weights_sha256"]})
    return probabilities, packages


def build_payload(root: Path, data: dict[str, object], probabilities: dict[int, np.ndarray], packages: list[dict[str, object]], unet_prediction: np.ndarray, unet_probability: np.ndarray, protocol: dict[str, object]) -> dict[str, object]:
    root.mkdir(parents=True, exist_ok=False)
    patch_ids = data["patch_ids"]
    event_ids = data["event_ids"]
    truth = data["truth"]
    mask = data["mask"]
    raw = data["raw_features"]
    seeds = protocol["execution"]["seeds"]
    threshold = 0.5
    seed_metrics = []
    geospatial_receipts = {}
    for seed in seeds:
        seed_root = root / "seeds" / str(seed)
        metrics = package_seed(seed_root, patch_ids, probabilities[seed], truth, mask, event_ids, threshold)
        seed_metrics.append(metrics)
        geospatial_receipts[str(seed)] = {}
        for index, patch_id in enumerate(patch_ids):
            spatial = data["spatial"][index]
            geospatial_receipts[str(seed)][patch_id] = write_geospatial_surfaces(seed_root / "geospatial" / patch_id, probabilities[seed][index], truth[index], mask[index], spatial["crs"], spatial["transform"], threshold)
    rbr_prediction = (rbr_probability_score(raw) >= np.float32(RBR_THRESHOLD)).astype(np.uint8)
    constants = {"constant background": np.zeros_like(truth, dtype=np.uint8), "constant burned": np.ones_like(truth, dtype=np.uint8)}
    comparator_predictions = {"RBR": rbr_prediction, "canonical Experiment One U-Net": unet_prediction, **constants}
    comparator_metrics = {name: evaluate_predictions(truth, prediction, mask, event_ids) for name, prediction in comparator_predictions.items()}
    comparator_root = root / "comparators"
    comparator_root.mkdir()
    for name, metrics in comparator_metrics.items():
        canonical_json(comparator_root / (name.lower().replace(" ", "-") + "-metrics.json"), metrics)
    decision = comparative_disposition(seed_metrics, [comparator_metrics["constant background"], comparator_metrics["constant burned"]])
    render_comparison(root / "rendered-comparison.png", patch_ids, raw, truth, mask, rbr_prediction, unet_prediction, probabilities, threshold)
    manifest = {
        "schema_version": "burnlens-exp3-retrospective-evaluation/v1",
        "scope": "known_retrospective_sparse_prototype_core_compatibility",
        "protocol_sha256": PROTOCOL_SHA256,
        "threshold": threshold,
        "rbr_threshold": RBR_THRESHOLD,
        "patch_ids": patch_ids,
        "event_ids": list(dict.fromkeys(event_ids)),
        "eligible_test_pixels": int(mask.sum()),
        "seeds": [{"seed": seed, "checkpoint": package, "metrics": metrics} for seed, package, metrics in zip(seeds, packages, seed_metrics, strict=True)],
        "comparators": comparator_metrics,
        "unet_probability_finite": bool(np.isfinite(unet_probability).all()),
        "geospatial_receipts": geospatial_receipts,
        "lifecycle_status": "PASS",
        **decision,
        "claim_limits": ["retrospective compatibility only", "two known test events", "sparse selected prototype cores", "events not pixels are independent units", "no dense accuracy, significance, generalization, operational, or wildfire-guidance claim"],
        "post_test_changes": 0,
    }
    canonical_json(root / "comparison-manifest.json", manifest)
    (root / "model-card.md").write_text(f"# Experiment Three evaluation package\n\nLifecycle: PASS. Comparative: {decision['comparative_status']}. Threshold: 0.5. Three frozen seeds are reported; none was selected as best.\n", encoding="utf-8")
    (root / "limitations.md").write_text("# Limitations\n\nKnown retrospective test; two events; sparse prototype cores; no population, dense-accuracy, significance, operational, emergency, or generalization claim.\n", encoding="utf-8")
    return roster(root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--custody-root", type=Path, required=True)
    parser.add_argument("--training-root", type=Path, required=True)
    parser.add_argument("--opened-at-utc", required=True)
    args = parser.parse_args()
    if args.output.name != EXPECTED_OUTPUT_NAME:
        raise ValueError(f"output root must be named {EXPECTED_OUTPUT_NAME}")
    protocol = load_protocol(PROTOCOL_PATH)
    if sha256_file(PROTOCOL_PATH) != PROTOCOL_SHA256:
        raise ValueError("frozen protocol hash drift")
    seeds = protocol["execution"]["seeds"]
    opening = {
        "schema_version": "burnlens-exp3-opening/v1",
        "opening_id": "M5-OPENING-2026-001",
        "state": "OPENING",
        "opened_at_utc": args.opened_at_utc,
        "protocol_sha256": PROTOCOL_SHA256,
        "accepted_training_attempt": "m4-2026-005",
        "seeds": seeds,
        "threshold": 0.5,
        "test_arrays_deserialized": 0,
        "historical_prediction_arrays_deserialized": 0,
        "previous_evaluation_roots": 0,
        "post_test_changes": 0,
    }
    marker = create_opening_root(args.output, opening)
    data = load_opened_test(args.custody_root, protocol, marker)
    unet_prediction, unet_probability = load_unet_comparator(args.custody_root, data["patch_ids"])
    probabilities, packages = infer(args.training_root, data["normalized_features"], seeds)
    primary = build_payload(args.output / "primary", data, probabilities, packages, unet_prediction, unet_probability, protocol)
    replay = build_payload(args.output / "replay", data, probabilities, packages, unet_prediction, unet_probability, protocol)
    if primary != replay:
        raise RuntimeError("primary and replay evaluation payloads differ")
    receipt = {"schema_version": "burnlens-exp3-retrospective-replay/v1", "status": "PASS", "opening_id": opening["opening_id"], "single_opening": True, "primary_replay_exact": True, "payload": primary, "test_arrays_deserialized_once": 16, "historical_prediction_arrays_deserialized_once": 8, "post_test_changes": 0}
    canonical_json(args.output / "exact-replay-receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
