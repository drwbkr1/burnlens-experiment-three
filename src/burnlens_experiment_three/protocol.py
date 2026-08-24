"""Frozen Experiment Three protocol loading and fail-closed validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


PROTOCOL_ID = "EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_protocol(path: Path) -> dict[str, Any]:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    validate_protocol(protocol)
    return protocol


def validate_protocol(protocol: dict[str, Any]) -> None:
    if protocol.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("unexpected protocol_id")
    if protocol.get("status") not in {"frozen_candidate", "frozen"}:
        raise ValueError("protocol must be a frozen candidate or frozen")
    model = protocol["model"]
    if model["architecture_id"] != "burnlens-exp3-pointwise-6x8x8x1-v1":
        raise ValueError("architecture drift")
    if model["trainable_parameters"] != 137:
        raise ValueError("parameter-count drift")
    execution = protocol["execution"]
    if execution["device"] != "cpu" or execution["dtype"] != "float32":
        raise ValueError("execution route drift")
    if execution["seeds"] != [20260725, 20260726, 20260727]:
        raise ValueError("seed drift")
    if execution["primary_seed"] != 20260725:
        raise ValueError("primary seed drift")
    optimizer = execution["optimizer"]
    expected_optimizer = {
        "family": "Adam",
        "learning_rate": 0.001,
        "betas": [0.9, 0.999],
        "epsilon": 1e-8,
        "weight_decay": 0.0,
        "amsgrad": False,
    }
    if optimizer != expected_optimizer:
        raise ValueError("optimizer drift")
    if execution["epochs"]["maximum"] != 200 or execution["epochs"]["patience"] != 25:
        raise ValueError("training budget drift")
    if protocol["data"]["batching"] != "one fixed four-patch batch per role; batch_size=4":
        raise ValueError("batching drift")
    roles = protocol["data"]["roles"]
    if {name: len(value["patch_ids"]) for name, value in roles.items()} != {
        "train": 4,
        "validation": 4,
        "test": 4,
    }:
        raise ValueError("patch roster drift")
    if any(len(value["event_group_ids"]) != 2 for value in roles.values()):
        raise ValueError("event roster drift")
    grid = protocol["threshold_selection"]["grid"]
    if grid != {
        "start": 0.01,
        "stop": 0.99,
        "step": 0.01,
        "integer_construction": "k/100 for k=1..99",
    }:
        raise ValueError("threshold grid drift")
    prohibited = set(model["prohibited"])
    required_prohibitions = {
        "augmentation",
        "positive class weighting",
        "BatchNorm",
        "dropout",
        "ensemble",
        "pretraining",
        "architecture search",
        "hyperparameter search",
    }
    if prohibited != required_prohibitions:
        raise ValueError("prohibited method set drift")


def verify_binding(root: Path, binding: dict[str, Any]) -> None:
    relative = binding.get("path") or binding.get("custody_relative_path")
    if not relative:
        raise ValueError("binding lacks path")
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    if binding.get("hash_mode") == "repository_text_canonical_lf":
        content = path.read_bytes().replace(b"\r\n", b"\n")
        if len(content) != binding["canonical_lf_bytes"]:
            raise ValueError(f"canonical binding size mismatch: {relative}")
        observed_hash = hashlib.sha256(content).hexdigest()
    else:
        if "bytes" in binding and path.stat().st_size != binding["bytes"]:
            raise ValueError(f"binding size mismatch: {relative}")
        observed_hash = sha256_file(path)
    if observed_hash != binding["sha256"]:
        raise ValueError(f"binding hash mismatch: {relative}")
