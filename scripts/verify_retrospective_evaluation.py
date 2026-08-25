#!/usr/bin/env python3
"""Independently verify the immutable M5 retrospective evaluation package."""

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
import rasterio
import torch

from burnlens_experiment_three.checkpoint import load_state_dict_package
from burnlens_experiment_three.evaluation import evaluate_predictions, load_opened_test, load_unet_comparator, rbr_probability_score, sha256_file
from burnlens_experiment_three.model import FixedBurnChangeDetector
from burnlens_experiment_three.protocol import load_protocol
from burnlens_experiment_three.training import configure


PROTOCOL_PATH = ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
RBR_THRESHOLD = 0.041043221950531006


def files(root: Path) -> dict[str, tuple[int, str]]:
    return {path.relative_to(root).as_posix(): (path.stat().st_size, sha256_file(path)) for path in root.rglob("*") if path.is_file()}


def verify(root: Path, custody_root: Path, training_root: Path) -> dict[str, object]:
    opening = json.loads((root / "opening-receipt.json").read_text(encoding="utf-8"))
    receipt = json.loads((root / "exact-replay-receipt.json").read_text(encoding="utf-8"))
    if opening.get("opening_id") != "M5-OPENING-2026-001" or opening.get("previous_evaluation_roots") != 0 or receipt.get("single_opening") is not True:
        raise RuntimeError("single-opening receipt drift")
    primary_files = files(root / "primary")
    replay_files = files(root / "replay")
    if primary_files != replay_files:
        raise RuntimeError("primary/replay bytes differ")
    expected = {item["path"]: (item["bytes"], item["sha256"]) for item in receipt["payload"]["files"]}
    if primary_files != expected:
        raise RuntimeError("evaluation payload roster drift")
    protocol = load_protocol(PROTOCOL_PATH)
    data = load_opened_test(custody_root, protocol, root / "opening-receipt.json")
    unet_prediction, _ = load_unet_comparator(custody_root, data["patch_ids"])
    probabilities = {}
    inputs = torch.from_numpy(data["normalized_features"])
    for seed in protocol["execution"]["seeds"]:
        configure(seed)
        model = FixedBurnChangeDetector()
        load_state_dict_package(model, training_root / f"seed-{seed}" / "selected-checkpoint")
        model.eval()
        with torch.inference_mode():
            value = torch.sigmoid(model(inputs)).cpu().numpy()[:, 0].astype(np.float32)
        probabilities[seed] = value
        seed_root = root / "primary" / "seeds" / str(seed)
        with np.load(seed_root / "test-probabilities.npz", allow_pickle=False) as archive:
            for index, patch_id in enumerate(data["patch_ids"]):
                if not np.array_equal(archive[patch_id], value[index]):
                    raise RuntimeError(f"probability replay drift: {seed}/{patch_id}")
        with np.load(seed_root / "test-predictions.npz", allow_pickle=False) as archive:
            predictions = np.stack([archive[patch_id] for patch_id in data["patch_ids"]])
        recalculated = evaluate_predictions(data["truth"], predictions, data["mask"], data["event_ids"])
        recorded = json.loads((seed_root / "per-seed-metrics.json").read_text(encoding="utf-8"))
        if recorded["events"] != recalculated["events"] or recorded["aggregate"] != recalculated["aggregate"]:
            raise RuntimeError(f"metric replay drift: {seed}")
        for index, patch_id in enumerate(data["patch_ids"]):
            geo = seed_root / "geospatial" / patch_id
            expected_arrays = {
                "probability.tif": np.where(data["mask"][index], value[index], np.float32(-9999.0)).astype(np.float32),
                "class.tif": np.where(data["mask"][index], (value[index] >= 0.5).astype(np.uint8), np.uint8(255)).astype(np.uint8),
            }
            truth = data["truth"][index]; mask = data["mask"][index]; prediction = value[index] >= 0.5
            error = np.full(truth.shape, 255, dtype=np.uint8); error[mask & (prediction == truth)] = 0; error[mask & prediction & (truth == 0)] = 1; error[mask & (~prediction) & (truth == 1)] = 2
            expected_arrays["error.tif"] = error
            for filename, expected_array in expected_arrays.items():
                with rasterio.open(geo / filename) as dataset:
                    if not np.array_equal(dataset.read(1), expected_array) or dataset.crs.to_string() != data["spatial"][index]["crs"]:
                        raise RuntimeError(f"GeoTIFF replay drift: {seed}/{patch_id}/{filename}")
    rbr = (rbr_probability_score(data["raw_features"]) >= np.float32(RBR_THRESHOLD)).astype(np.uint8)
    controls = {
        "rbr-metrics.json": rbr,
        "canonical-experiment-one-u-net-metrics.json": unet_prediction,
        "constant-background-metrics.json": np.zeros_like(data["truth"], dtype=np.uint8),
        "constant-burned-metrics.json": np.ones_like(data["truth"], dtype=np.uint8),
    }
    for filename, prediction in controls.items():
        expected_metrics = evaluate_predictions(data["truth"], prediction, data["mask"], data["event_ids"])
        observed_metrics = json.loads((root / "primary" / "comparators" / filename).read_text(encoding="utf-8"))
        if expected_metrics != observed_metrics:
            raise RuntimeError(f"comparator replay drift: {filename}")
    with Image.open(root / "primary" / "rendered-comparison.png") as image:
        if image.format != "PNG" or image.mode != "RGB" or image.width < 1200 or image.height < 1000:
            raise RuntimeError("rendered comparison inspection failed")
        render = {"format": image.format, "mode": image.mode, "size": list(image.size)}
    manifest = json.loads((root / "primary" / "comparison-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("lifecycle_status") != "PASS" or manifest.get("comparative_status") not in {"PASS", "FAIL"} or manifest.get("post_test_changes") != 0:
        raise RuntimeError("terminal disposition drift")
    return {"status": "PASS", "opening_id": opening["opening_id"], "single_opening": True, "primary_replay_exact": True, "payload_files": len(primary_files), "payload_bytes": sum(size for size, _ in primary_files.values()), "payload_roster_sha256": receipt["payload"]["roster_sha256"], "seeds": list(probabilities), "test_arrays": 16, "historical_prediction_arrays": 8, "geotiffs_reopened": 36, "render": render, "lifecycle_status": manifest["lifecycle_status"], "comparative_status": manifest["comparative_status"], "post_test_changes": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--custody-root", type=Path, required=True)
    parser.add_argument("--training-root", type=Path, required=True)
    parser.add_argument("--inspect-geospatial", action="store_true")
    parser.add_argument("--inspect-rendered", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.custody_root, args.training_root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
