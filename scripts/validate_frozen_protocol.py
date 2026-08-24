#!/usr/bin/env python3
"""Validate the frozen protocol and its admitted metadata bindings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "burnlens_experiment_three"
sys.path.insert(0, str(SOURCE))

from protocol import load_protocol, verify_binding  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--custody-root",
        type=Path,
        help="Optional controlled custody root; verifies metadata/comparator files only.",
    )
    args = parser.parse_args()
    path = ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
    protocol = load_protocol(path)
    for name in ("admission_manifest", "runtime_activation", "synthetic_preflight"):
        verify_binding(ROOT, protocol["bindings"][name])
    verified = ["admission_manifest", "runtime_activation", "synthetic_preflight"]
    if args.custody_root:
        for name in (
            "dataset_manifest",
            "whole_event_split",
            "train_normalization",
            "rbr_comparator",
            "unet_comparator",
        ):
            verify_binding(args.custody_root, protocol["bindings"][name])
            verified.append(name)
    print(json.dumps({"status": "PASS", "protocol_id": protocol["protocol_id"], "verified_bindings": verified}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
