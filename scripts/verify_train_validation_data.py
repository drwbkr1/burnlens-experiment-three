#!/usr/bin/env python3
"""Verify and decode only the frozen train and validation roles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from burnlens_experiment_three.data import load_frozen_role  # noqa: E402
from burnlens_experiment_three.protocol import load_protocol  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--custody-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    protocol_path = ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
    protocol = load_protocol(protocol_path)
    train = load_frozen_role(args.custody_root, protocol, "train")
    validation = load_frozen_role(args.custody_root, protocol, "validation")
    receipt = {
        "schema_version": "1.0",
        "receipt_id": "EXPERIMENT-THREE-M4-TRAIN-VALIDATION-DATA-2026-001",
        "status": "pass",
        "protocol_id": protocol["protocol_id"],
        "roles_decoded": ["train", "validation"],
        "test_arrays_listed_or_decoded": 0,
        "test_values_opened": False,
        "train": train.receipt,
        "validation": validation.receipt,
        "scientific_output": False,
        "training_runs": 0,
        "checkpoints": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), "test_values_opened": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
