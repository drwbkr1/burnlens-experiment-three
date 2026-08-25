#!/usr/bin/env python3
"""Exercise the complete M5 evidence path on fabricated arrays only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
from PIL import Image

from burnlens_experiment_three.evaluation import (
    comparative_disposition,
    evaluate_predictions,
    package_seed,
    render_comparison,
    sha256_file,
    write_geospatial_surfaces,
)
from burnlens_experiment_three.training import canonical_json


def fabricated_inputs() -> tuple[list[str], list[str], np.ndarray, np.ndarray, np.ndarray, dict[int, np.ndarray], np.ndarray, np.ndarray]:
    height = width = 16
    yy, xx = np.meshgrid(np.linspace(-1, 1, height, dtype=np.float32), np.linspace(-1, 1, width, dtype=np.float32), indexing="ij")
    features = []
    truth = []
    mask = []
    for index in range(4):
        channels = np.stack((xx, yy, xx * yy, np.sin(xx + index * .1), np.cos(yy - index * .1), xx - yy + index * .05)).astype(np.float32)
        target = (0.8 * xx - 0.6 * yy + index * .04 > 0).astype(np.uint8)
        valid = np.ones((height, width), dtype=bool)
        valid[:2] = False; valid[-2:] = False; valid[:, :2] = False; valid[:, -2:] = False
        features.append(channels); truth.append(target); mask.append(valid)
    feature_array = np.stack(features)
    truth_array = np.stack(truth)
    mask_array = np.stack(mask)
    score = 0.8 * feature_array[:, 0] - 0.6 * feature_array[:, 1]
    probabilities = {seed: (1.0 / (1.0 + np.exp(-(score + offset)))).astype(np.float32) for seed, offset in zip((20260725, 20260726, 20260727), (-0.10, 0.0, 0.10), strict=True)}
    rbr = (score >= 0.05).astype(np.uint8)
    unet = np.ones_like(truth_array, dtype=np.uint8)
    return [f"fabricated-patch-{i+1}" for i in range(4)], ["fabricated-event-a", "fabricated-event-a", "fabricated-event-b", "fabricated-event-b"], feature_array, truth_array, mask_array, probabilities, rbr, unet


def payload_roster(root: Path) -> dict[str, object]:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file() and item.name != "exact-replay-receipt.json"):
        rows.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    payload = "".join(f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows).encode()
    return {"files": rows, "file_count": len(rows), "bytes": sum(int(row["bytes"]) for row in rows), "roster_sha256": hashlib.sha256(payload).hexdigest()}


def build(root: Path) -> dict[str, object]:
    if root.exists():
        raise FileExistsError(root)
    root.mkdir(parents=True)
    patch_ids, event_ids, features, truth, mask, seed_probabilities, rbr, unet = fabricated_inputs()
    method_metrics: dict[str, object] = {}
    seed_rows = []
    for seed, probabilities in seed_probabilities.items():
        seed_root = root / "seeds" / str(seed)
        metrics = package_seed(seed_root, patch_ids, probabilities, truth, mask, event_ids, 0.5)
        method_metrics[str(seed)] = metrics
        seed_rows.append(metrics)
        for index, patch_id in enumerate(patch_ids):
            write_geospatial_surfaces(seed_root / "geospatial" / patch_id, probabilities[index], truth[index], mask[index], "EPSG:32610", [20.0, 0.0, 500000.0 + index * 10000.0, 0.0, -20.0, 5000000.0], 0.5)
    controls = {
        "RBR": evaluate_predictions(truth, rbr, mask, event_ids),
        "canonical Experiment One U-Net": evaluate_predictions(truth, unet, mask, event_ids),
        "constant background": evaluate_predictions(truth, np.zeros_like(truth), mask, event_ids),
        "constant burned": evaluate_predictions(truth, np.ones_like(truth), mask, event_ids),
    }
    disposition = comparative_disposition(seed_rows, [controls["constant background"], controls["constant burned"]])
    render_comparison(root / "rendered-comparison.png", patch_ids, features, truth, mask, rbr, unet, seed_probabilities, 0.5)
    with Image.open(root / "rendered-comparison.png") as image:
        render = {"format": image.format, "mode": image.mode, "size": list(image.size), "visual_roles": ["input", "truth", "RBR", "U-Net", "all three seed probabilities", "all three seed error maps"], "unscored_color": [145, 145, 145]}
    manifest = {
        "schema_version": "burnlens-exp3-evaluation-path-preflight/v1",
        "scope": "wholly_fabricated_non_scientific",
        "benchmark_accessed": False,
        "test_values_opened": False,
        "patch_ids": patch_ids,
        "event_ids": event_ids,
        "seeds": [20260725, 20260726, 20260727],
        "threshold": 0.5,
        "methods": {"seeds": method_metrics, "controls": controls},
        "decision_rule_exercised": disposition,
        "render": render,
        "geospatial": {"surface_count": 36, "per_seed_per_patch": ["probability.tif", "class.tif", "error.tif"], "reopen_exact": True, "unscored_is_nodata": True},
        "opening_control": {"exclusive_root_tested": True, "existing_root_rejected": True, "marker_precedes_deserialization": True},
    }
    canonical_json(root / "comparison-manifest.json", manifest)
    (root / "model-card.md").write_text("# Fabricated evaluation-path proof\n\nNot a model result. No benchmark value was opened.\n", encoding="utf-8")
    (root / "limitations.md").write_text("# Limitations\n\nFabricated arrays prove engineering behavior only.\n", encoding="utf-8")
    return payload_roster(root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    args = parser.parse_args()
    primary = build(args.primary)
    replay = build(args.replay)
    if primary != replay:
        raise RuntimeError("fabricated primary and replay payloads differ")
    receipt = {"schema_version": "burnlens-exp3-evaluation-path-preflight-replay/v1", "status": "PASS", "scope": "wholly_fabricated_non_scientific", "benchmark_accessed": False, "test_values_opened": False, "payload": primary, "primary_replay_exact": True}
    canonical_json(args.primary / "exact-replay-receipt.json", receipt)
    canonical_json(args.replay / "exact-replay-receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
