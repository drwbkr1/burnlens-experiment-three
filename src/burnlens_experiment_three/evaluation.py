"""Frozen metric, geospatial, render, and one-opening primitives for M5."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from statistics import median
from typing import Any, Mapping, Sequence

import numpy as np
from PIL import Image, ImageDraw
import rasterio
from rasterio.transform import Affine

from .metrics import aggregate_events, event_metrics
from .training import canonical_json, deterministic_npz


UNSCORED = np.uint8(255)
DATASET_MANIFEST_RELATIVE = Path("benchmark/experiment-one/samples/datasets/burnlens-dataset-v0.1.0/DATASET-MANIFEST.json")
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ADMISSION_MANIFEST = REPOSITORY_ROOT / "records/intake/EXPERIMENT-ONE-BENCHMARK-ADMISSION-MANIFEST-2026-001.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_opening_root(root: Path, receipt: Mapping[str, Any]) -> Path:
    """Atomically consume the sole sealed-to-open transition."""

    root.mkdir(parents=True, exist_ok=False)
    marker = root / "opening-receipt.json"
    canonical_json(marker, dict(receipt))
    return marker


def load_opened_test(custody_root: Path, protocol: Mapping[str, Any], opening_marker: Path) -> dict[str, Any]:
    """Load the exact test only after an immutable opening marker exists."""

    if opening_marker.name != "opening-receipt.json" or not opening_marker.is_file():
        raise PermissionError("valid opening marker is required before test deserialization")
    opening = json.loads(opening_marker.read_text(encoding="utf-8"))
    if opening.get("state") != "OPENING" or opening.get("test_arrays_deserialized") != 0:
        raise PermissionError("opening marker state is invalid")
    binding = protocol["bindings"]["dataset_manifest"]
    manifest_path = custody_root / binding["custody_relative_path"]
    if manifest_path != custody_root / DATASET_MANIFEST_RELATIVE or manifest_path.stat().st_size != binding["bytes"] or sha256_file(manifest_path) != binding["sha256"]:
        raise ValueError("dataset manifest binding drift")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = protocol["data"]["roles"]["test"]
    patch_ids = list(declared["patch_ids"])
    event_ids = list(declared["event_group_ids"])
    patches = {item["patch_id"]: item for item in manifest["patches"]}
    event_index = {event: index for index, event in enumerate(event_ids)}
    features_rows, state_rows, mask_rows, valid_rows, patch_events, spatial = [], [], [], [], [], []
    files = []
    for patch_id in patch_ids:
        patch = patches[patch_id]
        if patch["split_role"] != "test" or patch["event_group_id"] not in event_index:
            raise ValueError(f"test role drift: {patch_id}")
        declared_files = {Path(item["path"]).name: item for item in patch["files"]}
        arrays = {}
        for filename in ("features.npy", "input_valid.npy", "loss_mask.npy", "state.npy"):
            item = declared_files[filename]
            path = manifest_path.parent / item["path"]
            if path.stat().st_size != item["bytes"] or sha256_file(path) != item["sha256"]:
                raise ValueError(f"test array identity drift: {patch_id}/{filename}")
            arrays[filename] = np.load(path, allow_pickle=False)
            files.append({"path": item["path"], "bytes": item["bytes"], "sha256": item["sha256"]})
        features = arrays["features.npy"]
        state = arrays["state.npy"]
        loss_mask = arrays["loss_mask.npy"]
        input_valid = arrays["input_valid.npy"]
        if features.shape != (6, 64, 64) or features.dtype != np.float32 or any(array.shape != (64, 64) or array.dtype != np.uint8 for array in (state, loss_mask, input_valid)):
            raise ValueError(f"test schema drift: {patch_id}")
        expected_mask = np.isin(state, (0, 1)) & input_valid.astype(bool)
        if not np.array_equal(loss_mask.astype(bool), expected_mask):
            raise ValueError(f"test mask semantics drift: {patch_id}")
        features_rows.append(features); state_rows.append(state); mask_rows.append(loss_mask.astype(bool)); valid_rows.append(input_valid.astype(bool)); patch_events.append(patch["event_group_id"])
        spatial.append({"patch_id": patch_id, "crs": patch["crs"], "transform": patch["transform"]})
    raw = np.stack(features_rows)
    valid = np.stack(valid_rows)
    means = np.asarray(protocol["data"]["normalization"]["means"], dtype=np.float32).reshape(1, 6, 1, 1)
    stds = np.asarray(protocol["data"]["normalization"]["population_stds"], dtype=np.float32).reshape(1, 6, 1, 1)
    normalized = np.where(valid[:, None], (raw - means) / np.maximum(stds, np.float32(1e-6)), np.float32(0.0)).astype(np.float32)
    states = np.stack(state_rows)
    masks = np.stack(mask_rows)
    if int(masks.sum()) != int(declared["core_pixels"]) or not np.isfinite(normalized).all():
        raise ValueError("test core count or normalization drift")
    return {"patch_ids": patch_ids, "event_ids": patch_events, "raw_features": raw, "normalized_features": normalized, "truth": (states == 1).astype(np.uint8), "mask": masks, "input_valid": valid, "spatial": spatial, "verified_files": files}


def load_unet_comparator(custody_root: Path, patch_ids: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    base = custody_root / "benchmark/experiment-one/samples/evaluation/phase-three/bounded-unet-test-v0.1.0/predictions"
    admission = json.loads(ADMISSION_MANIFEST.read_text(encoding="utf-8"))
    identities = {item["destination_relative_path"]: item["expected"] for item in admission["assets"]}
    predictions, probabilities = [], []
    for patch_id in patch_ids:
        prediction_path = base / patch_id / "prediction.npy"
        probability_path = base / patch_id / "probability.npy"
        for path in (prediction_path, probability_path):
            relative = path.relative_to(custody_root / "benchmark").as_posix()
            expected = identities[relative]
            if path.stat().st_size != expected["size_bytes"] or sha256_file(path) != expected["sha256"]:
                raise ValueError(f"U-Net comparator identity drift: {relative}")
        prediction = np.load(prediction_path, allow_pickle=False)
        probability = np.load(probability_path, allow_pickle=False)
        if prediction.shape != (64, 64) or prediction.dtype != np.uint8 or probability.shape != (64, 64) or probability.dtype != np.float32:
            raise ValueError(f"U-Net comparator schema drift: {patch_id}")
        predictions.append(prediction); probabilities.append(probability)
    return np.stack(predictions), np.stack(probabilities)


def serialize_event_metrics(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "classes": {str(key): asdict(item) | {"dice": item.dice, "iou": item.iou} for key, item in value["classes"].items()},
        "class_macro_dice": value["class_macro_dice"],
        "class_macro_iou": value["class_macro_iou"],
        "predicted_burn_prevalence": value["predicted_burn_prevalence"],
        "nonconstant": value["nonconstant"],
    }


def evaluate_predictions(
    truth: np.ndarray,
    prediction: np.ndarray,
    mask: np.ndarray,
    patch_event_ids: Sequence[str],
) -> dict[str, Any]:
    if truth.shape != prediction.shape or truth.shape != mask.shape:
        raise ValueError("truth, prediction, and mask shapes must match")
    if truth.ndim != 3 or len(patch_event_ids) != truth.shape[0]:
        raise ValueError("expected patch-major [N,H,W] arrays")
    if not set(np.unique(truth[mask])).issubset({0, 1}) or not set(np.unique(prediction[mask])).issubset({0, 1}):
        raise ValueError("eligible truth and prediction must be binary")
    events: list[dict[str, Any]] = []
    for event_id in dict.fromkeys(patch_event_ids):
        indices = [index for index, value in enumerate(patch_event_ids) if value == event_id]
        eligible_truth = np.concatenate([truth[index][mask[index]].astype(np.uint8) for index in indices])
        eligible_prediction = np.concatenate([prediction[index][mask[index]].astype(np.uint8) for index in indices])
        metrics = serialize_event_metrics(event_metrics(eligible_truth.tolist(), eligible_prediction.tolist()))
        events.append({"event_group_id": event_id, "eligible_pixels": int(eligible_truth.size), **metrics})
    aggregate = aggregate_events(events)
    total_eligible = int(mask.sum())
    aggregate["predicted_burn_prevalence"] = float(prediction[mask].mean())
    aggregate["eligible_pixels"] = total_eligible
    aggregate["all_events_nonconstant"] = all(bool(item["nonconstant"]) for item in events)
    return {"events": events, "aggregate": aggregate}


def masked_bce(probabilities: np.ndarray, truth: np.ndarray, mask: np.ndarray) -> float:
    selected = np.clip(probabilities[mask].astype(np.float64), 1e-12, 1.0 - 1e-12)
    target = truth[mask].astype(np.float64)
    if selected.size == 0 or not np.isfinite(selected).all():
        raise ValueError("eligible probabilities must be nonempty and finite")
    return float(np.mean(-(target * np.log(selected) + (1.0 - target) * np.log(1.0 - selected))))


def rbr_probability_score(features: np.ndarray) -> np.ndarray:
    if features.ndim != 4 or features.shape[1] != 6:
        raise ValueError("RBR expects [N,6,H,W] features")
    pre_b8a, pre_b12 = features[:, 1], features[:, 2]
    post_b8a, post_b12 = features[:, 4], features[:, 5]
    pre_sum = pre_b8a + pre_b12
    post_sum = post_b8a + post_b12
    pre_nbr = np.divide(pre_b8a - pre_b12, pre_sum, out=np.zeros_like(pre_sum), where=pre_sum != 0)
    post_nbr = np.divide(post_b8a - post_b12, post_sum, out=np.zeros_like(post_sum), where=post_sum != 0)
    dnbr = pre_nbr - post_nbr
    denominator = pre_nbr + np.float32(1.001)
    return np.divide(dnbr, denominator, out=np.zeros_like(dnbr), where=denominator != 0).astype(np.float32)


def comparative_disposition(seed_metrics: Sequence[Mapping[str, Any]], constant_metrics: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if len(seed_metrics) != 3 or len(constant_metrics) != 2:
        raise ValueError("exactly three seeds and two constant controls are required")
    seed_iou = [float(item["aggregate"]["event_class_macro_iou"]) for item in seed_metrics]
    seed_worst_dice = [float(item["aggregate"]["worst_event_macro_dice"]) for item in seed_metrics]
    constant_iou = max(float(item["aggregate"]["event_class_macro_iou"]) for item in constant_metrics)
    constant_worst_dice = max(float(item["aggregate"]["worst_event_macro_dice"]) for item in constant_metrics)
    nonconstant = all(bool(item["aggregate"]["all_events_nonconstant"]) for item in seed_metrics)
    median_iou = float(median(seed_iou))
    median_worst_dice = float(median(seed_worst_dice))
    passed = nonconstant and median_iou > constant_iou and median_worst_dice > constant_worst_dice
    return {
        "comparative_status": "PASS" if passed else "FAIL",
        "every_seed_every_event_nonconstant": nonconstant,
        "three_seed_median_event_class_macro_iou": median_iou,
        "three_seed_median_worst_event_macro_dice": median_worst_dice,
        "strongest_constant_event_class_macro_iou": constant_iou,
        "strongest_constant_worst_event_macro_dice": constant_worst_dice,
        "strictly_beats_constants_on_both": median_iou > constant_iou and median_worst_dice > constant_worst_dice,
    }


def write_geospatial_surfaces(
    root: Path,
    probability: np.ndarray,
    truth: np.ndarray,
    mask: np.ndarray,
    crs: str,
    transform: Sequence[float],
    threshold: float,
) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    prediction = probability >= threshold
    error = np.full(truth.shape, UNSCORED, dtype=np.uint8)
    error[mask & (prediction == truth)] = 0
    error[mask & prediction & (truth == 0)] = 1
    error[mask & (~prediction) & (truth == 1)] = 2
    arrays = {
        "probability.tif": (np.where(mask, probability, np.float32(-9999.0)).astype(np.float32), "float32", -9999.0),
        "class.tif": (np.where(mask, prediction.astype(np.uint8), UNSCORED).astype(np.uint8), "uint8", 255),
        "error.tif": (error, "uint8", 255),
    }
    results: dict[str, Any] = {}
    affine = Affine(*[float(value) for value in transform])
    for filename, (array, dtype, nodata) in arrays.items():
        path = root / filename
        with rasterio.open(path, "w", driver="GTiff", height=array.shape[0], width=array.shape[1], count=1, dtype=dtype, crs=crs, transform=affine, nodata=nodata, compress="deflate") as dataset:
            dataset.write(array, 1)
            dataset.update_tags(SURFACE="RETROSPECTIVE_COMPATIBILITY", OPERATIONAL_USE="PROHIBITED", UNSCORED="NODATA")
        with rasterio.open(path) as dataset:
            reopened = dataset.read(1)
            if not np.array_equal(reopened, array) or dataset.crs.to_string() != crs or tuple(dataset.transform)[:6] != tuple(affine)[:6]:
                raise RuntimeError(f"GeoTIFF reopen mismatch: {filename}")
            results[filename] = {"bytes": path.stat().st_size, "sha256": sha256_file(path), "dtype": dataset.dtypes[0], "nodata": dataset.nodata, "crs": crs, "transform": list(tuple(affine)[:6]), "reopen_exact": True}
    return results


def _scaled_rgb(features: np.ndarray) -> np.ndarray:
    selected = features[[3, 4, 5]].transpose(1, 2, 0)
    low = np.percentile(selected, 2, axis=(0, 1), keepdims=True)
    high = np.percentile(selected, 98, axis=(0, 1), keepdims=True)
    scaled = np.clip((selected - low) / np.maximum(high - low, 1e-8), 0, 1)
    return np.round(scaled * 255).astype(np.uint8)


def _binary_rgb(values: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = np.zeros((*values.shape, 3), dtype=np.uint8)
    result[values.astype(bool)] = (230, 98, 52)
    result[~values.astype(bool)] = (35, 54, 70)
    result[~mask] = (145, 145, 145)
    return result


def _probability_rgb(values: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = np.stack((values * 255, (1 - np.abs(values - 0.5) * 2) * 180, (1 - values) * 255), axis=-1).round().astype(np.uint8)
    result[~mask] = (145, 145, 145)
    return result


def _error_rgb(truth: np.ndarray, prediction: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result = np.zeros((*truth.shape, 3), dtype=np.uint8)
    result[mask & (truth == prediction)] = (55, 145, 88)
    result[mask & (truth != prediction)] = (218, 55, 55)
    result[~mask] = (145, 145, 145)
    return result


def render_comparison(
    path: Path,
    patch_ids: Sequence[str],
    features: np.ndarray,
    truth: np.ndarray,
    mask: np.ndarray,
    rbr_prediction: np.ndarray,
    unet_prediction: np.ndarray,
    seed_probabilities: Mapping[int, np.ndarray],
    threshold: float,
) -> None:
    seeds = sorted(seed_probabilities)
    labels = ["POST INPUT", "TRUTH / MASK", "RBR", "U-NET"] + [label for seed in seeds for label in (f"S{seed} PROB", f"S{seed} ERROR")]
    scale, header, row_label = 8, 28, 240
    height, width = truth.shape[1:]
    canvas = Image.new("RGB", (row_label + len(labels) * width * scale, header + len(patch_ids) * height * scale), "white")
    draw = ImageDraw.Draw(canvas)
    for column, label in enumerate(labels):
        draw.text((row_label + column * width * scale + 4, 6), label, fill="black")
    for row, patch_id in enumerate(patch_ids):
        y = header + row * height * scale
        draw.text((4, y + 4), patch_id[:31], fill="black")
        panels = [_scaled_rgb(features[row]), _binary_rgb(truth[row], mask[row]), _binary_rgb(rbr_prediction[row], mask[row]), _binary_rgb(unet_prediction[row], mask[row])]
        for seed in seeds:
            probability = seed_probabilities[seed][row]
            panels.extend((_probability_rgb(probability, mask[row]), _error_rgb(truth[row], probability >= threshold, mask[row])))
        for column, panel in enumerate(panels):
            image = Image.fromarray(panel, mode="RGB").resize((width * scale, height * scale), resample=Image.Resampling.NEAREST)
            canvas.paste(image, (row_label + column * width * scale, y))
    canvas.save(path, format="PNG", optimize=False, compress_level=9)


def package_seed(root: Path, patch_ids: Sequence[str], probabilities: np.ndarray, truth: np.ndarray, mask: np.ndarray, event_ids: Sequence[str], threshold: float) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=False)
    predictions = (probabilities >= threshold).astype(np.uint8)
    deterministic_npz(root / "test-probabilities.npz", {patch_id: probabilities[index].astype(np.float32) for index, patch_id in enumerate(patch_ids)})
    deterministic_npz(root / "test-predictions.npz", {patch_id: predictions[index] for index, patch_id in enumerate(patch_ids)})
    metrics = evaluate_predictions(truth, predictions, mask, event_ids)
    metrics["masked_bce"] = masked_bce(probabilities, truth, mask)
    canonical_json(root / "per-seed-metrics.json", metrics)
    return metrics
