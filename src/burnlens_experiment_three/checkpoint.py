"""State-dict-only checkpoint helpers with explicit integrity metadata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

import torch
from torch import nn

from .model import ARCHITECTURE_ID, EXPECTED_PARAMETER_COUNT, parameter_count


def tensor_state_sha256(state: Mapping[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        tensor = state[name].detach().cpu().contiguous()
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(tensor.dtype).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(tuple(tensor.shape)).encode("ascii"))
        digest.update(b"\0")
        digest.update(tensor.numpy().tobytes())
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_state_dict_package(model: nn.Module, package_root: Path) -> dict[str, object]:
    if package_root.exists():
        raise FileExistsError(package_root)
    package_root.mkdir(parents=True)
    if parameter_count(model) != EXPECTED_PARAMETER_COUNT:
        raise ValueError("model does not match the fixed 137-parameter architecture")
    state = {name: tensor.detach().cpu().contiguous() for name, tensor in model.state_dict().items()}
    weights_path = package_root / "state_dict.pt"
    torch.save(state, weights_path)
    manifest = {
        "schema_version": "burnlens-exp3-state-dict-package/v1",
        "architecture_id": ARCHITECTURE_ID,
        "parameter_count": EXPECTED_PARAMETER_COUNT,
        "weights_file": weights_path.name,
        "weights_bytes": weights_path.stat().st_size,
        "weights_sha256": file_sha256(weights_path),
        "tensor_state_sha256": tensor_state_sha256(state),
        "serialization": "torch.save state_dict tensors only; reload requires weights_only=True",
    }
    manifest_path = package_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def load_state_dict_package(model: nn.Module, package_root: Path) -> dict[str, object]:
    manifest = json.loads((package_root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("architecture_id") != ARCHITECTURE_ID:
        raise ValueError("checkpoint architecture identity mismatch")
    if manifest.get("parameter_count") != EXPECTED_PARAMETER_COUNT:
        raise ValueError("checkpoint parameter count mismatch")
    weights_path = package_root / str(manifest["weights_file"])
    if file_sha256(weights_path) != manifest.get("weights_sha256"):
        raise ValueError("checkpoint file hash mismatch")
    state = torch.load(weights_path, map_location="cpu", weights_only=True)
    if not isinstance(state, dict) or not all(
        isinstance(name, str) and isinstance(tensor, torch.Tensor)
        for name, tensor in state.items()
    ):
        raise TypeError("weights-only checkpoint is not a tensor state dict")
    if tensor_state_sha256(state) != manifest.get("tensor_state_sha256"):
        raise ValueError("checkpoint tensor-state hash mismatch")
    model.load_state_dict(state, strict=True)
    return manifest
