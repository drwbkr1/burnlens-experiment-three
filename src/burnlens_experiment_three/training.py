"""Exact frozen train/validation lifecycle for Experiment Three."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
from statistics import median
from typing import Any
import zipfile
from io import BytesIO

import numpy as np
import torch

from .checkpoint import file_sha256, load_state_dict_package, tensor_state_sha256
from .data import BenchmarkBatch, load_frozen_role
from .losses import event_class_balanced_masked_bce
from .metrics import aggregate_events, event_metrics
from .model import FixedBurnChangeDetector
from .selection import EpochObservation, ThresholdScore, early_stop_epoch, select_checkpoint, select_shared_threshold, threshold_grid


def configure(seed: int) -> None:
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass
    torch.manual_seed(seed)


def tensor_sha256(tensor: torch.Tensor) -> str:
    return hashlib.sha256(tensor.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def canonical_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def deterministic_npz(path: Path, arrays: dict[str, np.ndarray]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(arrays):
            payload = BytesIO()
            np.lib.format.write_array(payload, np.asarray(arrays[name]), allow_pickle=False)
            info = zipfile.ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, payload.getvalue(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def save_training_checkpoint(model: torch.nn.Module, package_root: Path) -> dict[str, Any]:
    """Write the protocol-frozen weights.pt state-dict-only package."""

    if package_root.exists():
        raise FileExistsError(package_root)
    package_root.mkdir(parents=True)
    state = {name: tensor.detach().cpu().contiguous() for name, tensor in model.state_dict().items()}
    weights = package_root / "weights.pt"
    torch.save(state, weights)
    manifest = {
        "schema_version": "burnlens-exp3-state-dict-package/v1",
        "architecture_id": "burnlens-exp3-pointwise-6x8x8x1-v1",
        "parameter_count": 137,
        "weights_file": "weights.pt",
        "weights_bytes": weights.stat().st_size,
        "weights_sha256": file_sha256(weights),
        "tensor_state_sha256": tensor_state_sha256(state),
        "serialization": "torch.save state_dict tensors only; reload requires weights_only=True",
    }
    canonical_json(package_root / "manifest.json", manifest)
    return manifest


def evaluate_loss(model: torch.nn.Module, batch: BenchmarkBatch) -> tuple[float, torch.Tensor]:
    model.eval()
    with torch.inference_mode():
        logits = model(batch.inputs)
        loss = event_class_balanced_masked_bce(logits, batch.targets, batch.loss_mask, batch.event_ids)
    if not torch.isfinite(loss) or not torch.isfinite(logits).all():
        raise RuntimeError("nonfinite evaluation surface")
    return float(loss), torch.sigmoid(logits)


def train_seed(seed: int, train: BenchmarkBatch, validation: BenchmarkBatch, root: Path) -> dict[str, Any]:
    if root.exists():
        raise FileExistsError(root)
    root.mkdir(parents=True)
    configure(seed)
    model = FixedBurnChangeDetector()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0, amsgrad=False)
    initial_hash = tensor_state_sha256(model.state_dict())
    observations: list[EpochObservation] = []
    rows: list[dict[str, Any]] = []
    best_loss: float | None = None
    best_state: dict[str, torch.Tensor] | None = None
    first_gradient_norm: float | None = None
    first_step_hash: str | None = None

    for epoch in range(1, 201):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(train.inputs)
        loss = event_class_balanced_masked_bce(logits, train.targets, train.loss_mask, train.event_ids)
        if not torch.isfinite(loss):
            raise RuntimeError("nonfinite training loss")
        loss.backward()
        gradients = [parameter.grad for parameter in model.parameters()]
        if any(value is None for value in gradients):
            raise RuntimeError("missing gradient")
        norm = float(torch.sqrt(sum(value.detach().square().sum() for value in gradients if value is not None)))
        if not np.isfinite(norm) or norm <= 0.0:
            raise RuntimeError("invalid gradient norm")
        if epoch == 1:
            first_gradient_norm = norm
        optimizer.step()
        if epoch == 1:
            first_step_hash = tensor_state_sha256(model.state_dict())
            if first_step_hash == initial_hash:
                raise RuntimeError("first optimizer step did not change weights")
        train_loss, _ = evaluate_loss(model, train)
        validation_loss, _ = evaluate_loss(model, validation)
        observations.append(EpochObservation(epoch, validation_loss))
        rows.append({"epoch": epoch, "train_balanced_bce": train_loss, "validation_balanced_bce": validation_loss})
        if best_loss is None or validation_loss < best_loss:
            best_loss = validation_loss
            best_state = copy.deepcopy(model.state_dict())
        stop = early_stop_epoch(observations)
        if stop is not None:
            break

    selected = select_checkpoint(observations)
    if best_state is None or best_loss != selected.validation_loss:
        raise RuntimeError("checkpoint selection state mismatch")
    final_hash = tensor_state_sha256(model.state_dict())
    model.load_state_dict(best_state, strict=True)
    selected_hash = tensor_state_sha256(model.state_dict())
    package = save_training_checkpoint(model, root / "selected-checkpoint")
    selected_validation_loss, probabilities = evaluate_loss(model, validation)
    if selected_validation_loss != selected.validation_loss:
        raise RuntimeError("selected checkpoint validation loss drift")
    deterministic_npz(
        root / "validation-probabilities.npz",
        {patch_id: probabilities[index, 0].cpu().numpy().astype("<f4") for index, patch_id in enumerate(validation.patch_ids)},
    )
    history = {
        "seed": seed,
        "epochs_completed": len(rows),
        "early_stopped": len(rows) < 200,
        "selected_epoch": selected.epoch,
        "selected_validation_balanced_bce": selected.validation_loss,
        "initial_tensor_state_sha256": initial_hash,
        "first_step_tensor_state_sha256": first_step_hash,
        "final_tensor_state_sha256": final_hash,
        "selected_tensor_state_sha256": selected_hash,
        "first_gradient_norm": first_gradient_norm,
        "rows": rows,
    }
    canonical_json(root / "training-history.json", history)
    manifest = {
        "seed": seed,
        "status": "valid",
        "architecture_id": "burnlens-exp3-pointwise-6x8x8x1-v1",
        "parameter_count": 137,
        "train_patch_ids": list(train.patch_ids),
        "validation_patch_ids": list(validation.patch_ids),
        "selected_epoch": selected.epoch,
        "selected_validation_balanced_bce": selected.validation_loss,
        "checkpoint_tensor_state_sha256": package["tensor_state_sha256"],
        "process_scope": "fresh_isolated_subprocess_per_seed",
        "runtime": {
            "python": sys.version.split()[0],
            "torch": torch.__version__,
            "device": "cpu",
            "dtype": "float32",
            "num_threads": torch.get_num_threads(),
            "num_interop_threads": torch.get_num_interop_threads(),
        },
        "exception": None,
        "test_values_opened": False,
    }
    canonical_json(root / "run-manifest.json", manifest)
    return {"manifest": manifest, "history": history, "probabilities": probabilities}


def reload_seed(seed: int, package: Path, validation: BenchmarkBatch, output: Path) -> None:
    configure(seed)
    model = FixedBurnChangeDetector()
    manifest = load_state_dict_package(model, package)
    loss, probabilities = evaluate_loss(model, validation)
    canonical_json(output, {"tensor_state_sha256": manifest["tensor_state_sha256"], "validation_balanced_bce": loss, "probabilities_sha256": tensor_sha256(probabilities), "test_values_opened": False})


def select_threshold(results: dict[int, dict[str, Any]], validation: BenchmarkBatch) -> dict[str, Any]:
    scores: list[ThresholdScore] = []
    detail: list[dict[str, Any]] = []
    targets = validation.targets[:, 0].cpu().numpy().astype(np.uint8)
    masks = validation.loss_mask[:, 0].cpu().numpy().astype(bool)
    event_ids = validation.event_ids.cpu().numpy()
    for threshold in threshold_grid():
        minimum_dice: list[float] = []
        seed_ious: list[float] = []
        for seed in sorted(results):
            probabilities = results[seed]["probabilities"][:, 0].cpu().numpy()
            predictions = (probabilities >= threshold).astype(np.uint8)
            events = []
            for event_id in (0, 1):
                selector = event_ids == event_id
                truth = targets[selector][masks[selector]].tolist()
                predicted = predictions[selector][masks[selector]].tolist()
                event = event_metrics(truth, predicted)
                events.append(event)
                minimum_dice.append(float(event["class_macro_dice"]))
            seed_ious.append(aggregate_events(events)["event_class_macro_iou"])
        score = ThresholdScore(threshold, min(minimum_dice), median(seed_ious))
        scores.append(score)
        detail.append({"threshold": threshold, "minimum_seed_event_macro_dice": score.minimum_seed_event_macro_dice, "median_seed_event_class_macro_iou": score.median_seed_event_class_macro_iou})
    selected = select_shared_threshold(scores)
    return {"selected_threshold": selected.threshold, "ranking": ["maximum minimum seed-event macro Dice", "maximum median seed event-class macro IoU", "minimum distance to 0.5", "lower threshold"], "grid": detail, "test_values_opened": False}
