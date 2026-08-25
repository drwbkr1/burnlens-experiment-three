"""Fail-closed loader for the frozen Experiment One train/validation roles."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import torch


DATASET_RELATIVE = Path(
    "benchmark/experiment-one/samples/datasets/"
    "burnlens-dataset-v0.1.0/DATASET-MANIFEST.json"
)


@dataclass(frozen=True)
class BenchmarkBatch:
    role: str
    patch_ids: tuple[str, ...]
    event_group_ids: tuple[str, ...]
    event_ids: torch.Tensor
    inputs: torch.Tensor
    targets: torch.Tensor
    loss_mask: torch.Tensor
    input_valid: torch.Tensor
    receipt: dict[str, Any]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_frozen_role(
    custody_root: Path,
    protocol: dict[str, Any],
    role: str,
) -> BenchmarkBatch:
    """Load exactly train or validation; test is intentionally impossible here."""

    if role not in {"train", "validation"}:
        raise PermissionError("Milestone 4 loader permits train and validation only")
    binding = protocol["bindings"]["dataset_manifest"]
    manifest_path = custody_root / binding["custody_relative_path"]
    if manifest_path != custody_root / DATASET_RELATIVE:
        raise ValueError("dataset manifest path drift")
    if manifest_path.stat().st_size != binding["bytes"]:
        raise ValueError("dataset manifest size drift")
    if file_sha256(manifest_path) != binding["sha256"]:
        raise ValueError("dataset manifest hash drift")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = protocol["data"]["roles"][role]
    patch_ids = tuple(declared["patch_ids"])
    event_groups = tuple(declared["event_group_ids"])
    patches = {item["patch_id"]: item for item in manifest["patches"]}
    if any(patch_id not in patches for patch_id in patch_ids):
        raise ValueError("frozen patch missing from dataset manifest")

    features_rows: list[np.ndarray] = []
    state_rows: list[np.ndarray] = []
    mask_rows: list[np.ndarray] = []
    valid_rows: list[np.ndarray] = []
    numeric_event_ids: list[int] = []
    verified_files: list[dict[str, Any]] = []
    dataset_root = manifest_path.parent
    event_index = {name: index for index, name in enumerate(event_groups)}

    for patch_id in patch_ids:
        patch = patches[patch_id]
        if patch["split_role"] != role or patch["event_group_id"] not in event_index:
            raise ValueError(f"role or event drift for {patch_id}")
        declared_files = {Path(item["path"]).name: item for item in patch["files"]}
        arrays: dict[str, np.ndarray] = {}
        for filename in ("features.npy", "input_valid.npy", "loss_mask.npy", "state.npy"):
            item = declared_files[filename]
            path = dataset_root / item["path"]
            if path.stat().st_size != item["bytes"] or file_sha256(path) != item["sha256"]:
                raise ValueError(f"array identity drift: {patch_id}/{filename}")
            arrays[filename] = np.load(path, allow_pickle=False)
            verified_files.append(
                {"path": item["path"], "bytes": item["bytes"], "sha256": item["sha256"]}
            )
        features = arrays["features.npy"]
        input_valid = arrays["input_valid.npy"]
        loss_mask = arrays["loss_mask.npy"]
        state = arrays["state.npy"]
        if features.shape != (6, 64, 64) or features.dtype != np.float32:
            raise ValueError(f"feature schema drift: {patch_id}")
        if any(array.shape != (64, 64) or array.dtype != np.uint8 for array in (input_valid, loss_mask, state)):
            raise ValueError(f"mask/state schema drift: {patch_id}")
        if not set(np.unique(input_valid)).issubset({0, 1}) or not set(np.unique(loss_mask)).issubset({0, 1}):
            raise ValueError(f"nonbinary mask: {patch_id}")
        expected_loss = np.isin(state, (0, 1)) & input_valid.astype(bool)
        if not np.array_equal(loss_mask.astype(bool), expected_loss):
            raise ValueError(f"loss-mask semantics drift: {patch_id}")
        features_rows.append(features)
        state_rows.append(state)
        mask_rows.append(loss_mask)
        valid_rows.append(input_valid)
        numeric_event_ids.append(event_index[patch["event_group_id"]])

    features = np.stack(features_rows)
    valid = np.stack(valid_rows).astype(bool)
    means = np.asarray(protocol["data"]["normalization"]["means"], dtype=np.float32).reshape(1, 6, 1, 1)
    stds = np.asarray(protocol["data"]["normalization"]["population_stds"], dtype=np.float32).reshape(1, 6, 1, 1)
    normalized = (features - means) / np.maximum(stds, np.float32(1e-6))
    normalized = np.where(valid[:, None, :, :], normalized, np.float32(0.0)).astype(np.float32)
    if not np.isfinite(normalized).all():
        raise ValueError(f"nonfinite normalized {role} input")
    states = np.stack(state_rows)
    masks = np.stack(mask_rows).astype(bool)
    targets = (states == 1).astype(np.float32)
    loss_pixels = int(masks.sum())
    if loss_pixels != int(declared["core_pixels"]):
        raise ValueError(f"core pixel count drift for {role}")
    receipt = {
        "role": role,
        "patch_ids": list(patch_ids),
        "event_group_ids": list(event_groups),
        "verified_file_count": len(verified_files),
        "verified_bytes": sum(item["bytes"] for item in verified_files),
        "verified_files": verified_files,
        "feature_shape": list(normalized.shape),
        "target_shape": [4, 1, 64, 64],
        "loss_pixels": loss_pixels,
        "background_pixels": int(((states == 0) & masks).sum()),
        "burned_pixels": int(((states == 1) & masks).sum()),
    }
    return BenchmarkBatch(
        role=role,
        patch_ids=patch_ids,
        event_group_ids=event_groups,
        event_ids=torch.tensor(numeric_event_ids, dtype=torch.int64),
        inputs=torch.from_numpy(normalized),
        targets=torch.from_numpy(targets[:, None, :, :]),
        loss_mask=torch.from_numpy(masks[:, None, :, :]),
        input_valid=torch.from_numpy(valid[:, None, :, :]),
        receipt=receipt,
    )
