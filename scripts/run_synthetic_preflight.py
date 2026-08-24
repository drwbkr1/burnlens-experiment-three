#!/usr/bin/env python3
"""Execute the synthetic-only Experiment Three neural lifecycle preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import numpy as np
from PIL import Image, ImageDraw
import rasterio
from rasterio.transform import from_origin
import torch

from burnlens_experiment_three.checkpoint import (
    file_sha256,
    load_state_dict_package,
    save_state_dict_package,
    tensor_state_sha256,
)
from burnlens_experiment_three.losses import event_class_balanced_masked_bce
from burnlens_experiment_three.model import (
    ARCHITECTURE_ID,
    EXPECTED_PARAMETER_COUNT,
    FixedBurnChangeDetector,
    parameter_count,
)
from burnlens_experiment_three.synthetic import make_synthetic_batch


SEED = 20260725
TRAINING_STEPS = 120
LEARNING_RATE = 0.001


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_fingerprint(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def tensor_sha256(tensor: torch.Tensor) -> str:
    return sha256_bytes(tensor.detach().cpu().contiguous().numpy().tobytes())


def configure_runtime() -> None:
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.manual_seed(SEED)


def normalized_rgb(channels: np.ndarray) -> np.ndarray:
    selected = channels[[0, 1, 3]].transpose(1, 2, 0)
    minimum = selected.min(axis=(0, 1), keepdims=True)
    maximum = selected.max(axis=(0, 1), keepdims=True)
    scaled = (selected - minimum) / np.maximum(maximum - minimum, 1e-8)
    return np.round(scaled * 255.0).astype(np.uint8)


def render_panel(
    path: Path,
    inputs: torch.Tensor,
    targets: torch.Tensor,
    mask: torch.Tensor,
    probabilities: torch.Tensor,
) -> None:
    features = normalized_rgb(inputs[0].cpu().numpy())
    target = targets[0, 0].cpu().numpy().astype(bool)
    valid = mask[0, 0].cpu().numpy().astype(bool)
    probability = probabilities[0, 0].cpu().numpy()
    prediction = probability >= 0.5

    target_rgb = np.zeros((*target.shape, 3), dtype=np.uint8)
    target_rgb[target] = (240, 104, 56)
    target_rgb[~target] = (32, 51, 65)
    target_rgb[~valid] = (132, 132, 132)

    probability_rgb = np.stack(
        (
            np.round(probability * 255.0),
            np.round((1.0 - np.abs(probability - 0.5) * 2.0) * 180.0),
            np.round((1.0 - probability) * 255.0),
        ),
        axis=-1,
    ).astype(np.uint8)
    probability_rgb[~valid] = (132, 132, 132)

    error_rgb = np.zeros((*target.shape, 3), dtype=np.uint8)
    correct = prediction == target
    error_rgb[correct] = (55, 145, 88)
    error_rgb[~correct] = (218, 55, 55)
    error_rgb[~valid] = (132, 132, 132)

    scale = 6
    header = 24
    panels = [features, target_rgb, probability_rgb, error_rgb]
    labels = ["SYNTHETIC INPUT", "TARGET / MASK", "PROBABILITY", "0.5 ERROR MAP"]
    canvas = Image.new("RGB", (len(panels) * target.shape[1] * scale, target.shape[0] * scale + header), "white")
    draw = ImageDraw.Draw(canvas)
    for index, (panel, label) in enumerate(zip(panels, labels, strict=True)):
        image = Image.fromarray(panel, mode="RGB").resize(
            (target.shape[1] * scale, target.shape[0] * scale),
            resample=Image.Resampling.NEAREST,
        )
        x_offset = index * target.shape[1] * scale
        canvas.paste(image, (x_offset, header))
        draw.text((x_offset + 4, 6), label, fill="black")
    canvas.save(path, format="PNG", optimize=False, compress_level=9)


def write_probability_geotiff(path: Path, probabilities: torch.Tensor) -> dict[str, object]:
    array = probabilities[0, 0].detach().cpu().numpy().astype("float32")
    transform = from_origin(500000.0, 5000000.0, 30.0, 30.0)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=array.shape[0],
        width=array.shape[1],
        count=1,
        dtype="float32",
        crs="EPSG:32610",
        transform=transform,
        nodata=-9999.0,
        compress="deflate",
    ) as dataset:
        dataset.write(array, 1)
        dataset.update_tags(SURFACE="WHOLLY_SYNTHETIC_PREFLIGHT", OPERATIONAL_USE="PROHIBITED")
    with rasterio.open(path) as dataset:
        reopened = dataset.read(1)
        if not np.array_equal(reopened, array):
            raise RuntimeError("GeoTIFF reopen changed probability values")
        return {
            "driver": dataset.driver,
            "shape": [dataset.height, dataset.width],
            "count": dataset.count,
            "dtype": dataset.dtypes[0],
            "crs": dataset.crs.to_string(),
            "transform": list(dataset.transform)[:6],
            "nodata": dataset.nodata,
            "reopen_exact": True,
            "array_sha256": sha256_bytes(reopened.tobytes()),
        }


def reload_child(package_root: Path, result_path: Path) -> int:
    configure_runtime()
    batch = make_synthetic_batch()
    model = FixedBurnChangeDetector()
    manifest = load_state_dict_package(model, package_root)
    model.eval()
    with torch.inference_mode():
        logits = model(batch.inputs)
        probabilities = torch.sigmoid(logits)
    result = {
        "architecture_id": ARCHITECTURE_ID,
        "parameter_count": parameter_count(model),
        "tensor_state_sha256": manifest["tensor_state_sha256"],
        "logits_sha256": tensor_sha256(logits),
        "probabilities_sha256": tensor_sha256(probabilities),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "cuda_available": torch.cuda.is_available(),
    }
    if result_path.exists():
        raise FileExistsError(result_path)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


def run_preflight(output_root: Path) -> dict[str, object]:
    if output_root.exists():
        raise FileExistsError(output_root)
    output_root.mkdir(parents=True)
    configure_runtime()
    batch = make_synthetic_batch()
    model = FixedBurnChangeDetector()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    initial_state_hash = tensor_state_sha256(model.state_dict())
    model.train()
    optimizer.zero_grad(set_to_none=True)
    initial_logits = model(batch.inputs)
    initial_loss_tensor = event_class_balanced_masked_bce(
        initial_logits, batch.targets, batch.loss_mask, batch.event_ids
    )
    initial_loss_tensor.backward()
    gradients = [parameter.grad for parameter in model.parameters()]
    if any(gradient is None for gradient in gradients):
        raise RuntimeError("missing gradient")
    gradient_values = [gradient for gradient in gradients if gradient is not None]
    if not all(torch.isfinite(gradient).all() for gradient in gradient_values):
        raise RuntimeError("non-finite gradient")
    gradient_norm = math.sqrt(sum(float(gradient.square().sum()) for gradient in gradient_values))
    if gradient_norm <= 0.0:
        raise RuntimeError("zero gradient norm")
    initial_loss = float(initial_loss_tensor.detach())
    optimizer.step()
    first_step_state_hash = tensor_state_sha256(model.state_dict())
    if first_step_state_hash == initial_state_hash:
        raise RuntimeError("optimizer step did not change weights")

    history = [initial_loss]
    for _ in range(1, TRAINING_STEPS):
        optimizer.zero_grad(set_to_none=True)
        logits = model(batch.inputs)
        loss = event_class_balanced_masked_bce(
            logits, batch.targets, batch.loss_mask, batch.event_ids
        )
        if not torch.isfinite(loss):
            raise RuntimeError("non-finite synthetic loss")
        loss.backward()
        optimizer.step()
        history.append(float(loss.detach()))

    final_state_hash = tensor_state_sha256(model.state_dict())
    if final_state_hash == initial_state_hash:
        raise RuntimeError("final weights equal initial weights")
    if history[-1] >= history[0]:
        raise RuntimeError("synthetic loss did not decrease")

    model.eval()
    with torch.inference_mode():
        final_logits = model(batch.inputs)
        probabilities = torch.sigmoid(final_logits)
    logits_hash = tensor_sha256(final_logits)
    probabilities_hash = tensor_sha256(probabilities)

    package_root = output_root / "checkpoint-package"
    checkpoint_manifest = save_state_dict_package(model, package_root)
    reload_result_path = output_root / "fresh-process-reload.json"
    command = [
        sys.executable,
        "-I",
        str(Path(__file__).resolve()),
        "--reload-child",
        "--package-root",
        str(package_root),
        "--result-path",
        str(reload_result_path),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"fresh-process reload failed: stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    reload_result = json.loads(reload_result_path.read_text(encoding="utf-8"))
    if reload_result["logits_sha256"] != logits_hash:
        raise RuntimeError("fresh-process logits differ")
    if reload_result["probabilities_sha256"] != probabilities_hash:
        raise RuntimeError("fresh-process probabilities differ")

    geotiff_path = output_root / "synthetic-probability.tif"
    geotiff = write_probability_geotiff(geotiff_path, probabilities)
    render_path = output_root / "synthetic-comparison.png"
    render_panel(render_path, batch.inputs, batch.targets, batch.loss_mask, probabilities)
    history_path = output_root / "optimization-history.json"
    history_path.write_text(
        json.dumps({"step_loss": history}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    valid = batch.loss_mask
    prediction = probabilities >= 0.5
    correct = (prediction == batch.targets.bool()) & valid
    valid_count = int(valid.sum())
    diagnostic_accuracy = float(correct.sum()) / valid_count
    artifacts = {
        "checkpoint_manifest": {
            "path": "checkpoint-package/manifest.json",
            "sha256": file_sha256(package_root / "manifest.json"),
        },
        "checkpoint_weights": {
            "path": "checkpoint-package/state_dict.pt",
            "sha256": file_sha256(package_root / "state_dict.pt"),
        },
        "fresh_process_reload": {
            "path": reload_result_path.name,
            "sha256": file_sha256(reload_result_path),
        },
        "geotiff": {"path": geotiff_path.name, "sha256": file_sha256(geotiff_path)},
        "render": {"path": render_path.name, "sha256": file_sha256(render_path)},
        "history": {"path": history_path.name, "sha256": file_sha256(history_path)},
    }
    deterministic_surface = {
        "architecture_id": ARCHITECTURE_ID,
        "parameter_count": EXPECTED_PARAMETER_COUNT,
        "seed": SEED,
        "training_steps": TRAINING_STEPS,
        "learning_rate": LEARNING_RATE,
        "initial_state_sha256": initial_state_hash,
        "first_step_state_sha256": first_step_state_hash,
        "final_state_sha256": final_state_hash,
        "initial_loss": history[0],
        "final_loss": history[-1],
        "gradient_norm": gradient_norm,
        "logits_sha256": logits_hash,
        "probabilities_sha256": probabilities_hash,
        "synthetic_valid_accuracy": diagnostic_accuracy,
        "checkpoint_tensor_state_sha256": checkpoint_manifest["tensor_state_sha256"],
        "fresh_process_exact": True,
        "geotiff_array_sha256": geotiff["array_sha256"],
        "geotiff_sha256": artifacts["geotiff"]["sha256"],
        "render_sha256": artifacts["render"]["sha256"],
        "history_sha256": artifacts["history"]["sha256"],
    }
    receipt = {
        "schema_version": "burnlens-exp3-synthetic-preflight/v1",
        "scope": "wholly_synthetic_engineering_evidence_only",
        "benchmark_accessed": False,
        "scientific_output": False,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "torch": torch.__version__,
            "numpy": np.__version__,
            "rasterio": rasterio.__version__,
            "cuda_available": torch.cuda.is_available(),
            "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
            "torch_threads": torch.get_num_threads(),
        },
        "synthetic_fixture": {
            "shape": list(batch.inputs.shape),
            "target_shape": list(batch.targets.shape),
            "valid_locations": valid_count,
            "event_ids": batch.event_ids.tolist(),
            "generator": "deterministic coordinate and analytic functions; no benchmark bytes or values",
        },
        "checks": {
            "parameter_count_137": parameter_count(model) == EXPECTED_PARAMETER_COUNT,
            "finite_forward_loss_gradients": True,
            "nonzero_gradient_norm": gradient_norm > 0.0,
            "changed_weights_after_optimizer": first_step_state_hash != initial_state_hash,
            "loss_decreased": history[-1] < history[0],
            "safe_state_dict_only_package": True,
            "fresh_process_reload_exact": True,
            "geotiff_reopen_exact": geotiff["reopen_exact"],
            "render_created": True,
        },
        "geotiff": geotiff,
        "artifacts": artifacts,
        "deterministic_surface": deterministic_surface,
        "deterministic_fingerprint": json_fingerprint(deterministic_surface),
        "claim_limit": "Synthetic PASS proves engineering lifecycle behavior only; it is not training, evaluation, accuracy, generalization, superiority, or operational evidence.",
    }
    receipt_path = output_root / "preflight-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--reload-child", action="store_true")
    parser.add_argument("--package-root", type=Path)
    parser.add_argument("--result-path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.reload_child:
        if args.package_root is None or args.result_path is None:
            raise SystemExit("--reload-child requires --package-root and --result-path")
        return reload_child(args.package_root, args.result_path)
    if args.output_root is None:
        raise SystemExit("--output-root is required")
    receipt = run_preflight(args.output_root)
    print(json.dumps({
        "status": "pass",
        "output_root": str(args.output_root),
        "deterministic_fingerprint": receipt["deterministic_fingerprint"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
