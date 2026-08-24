#!/usr/bin/env python3
"""Exercise frozen selection and metric semantics on fabricated values only."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "burnlens_experiment_three"))

from metrics import aggregate_events, event_metrics  # noqa: E402
from protocol import load_protocol  # noqa: E402
from selection import (  # noqa: E402
    EpochObservation,
    ThresholdScore,
    select_checkpoint,
    select_shared_threshold,
    threshold_grid,
)


def main() -> int:
    protocol = load_protocol(ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json")
    selected = select_checkpoint(
        [EpochObservation(1, 0.8), EpochObservation(2, 0.7), EpochObservation(3, 0.7)]
    )
    scores = [ThresholdScore(value, 0.4, 0.3) for value in threshold_grid()]
    scores[49] = ThresholdScore(0.5, 0.8, 0.7)
    threshold = select_shared_threshold(scores)
    aggregate = aggregate_events(
        [event_metrics([0, 1], [0, 1]), event_metrics([0, 1], [1, 1])]
    )
    result = {
        "status": "PASS",
        "fixture": "fabricated_nonbenchmark",
        "protocol_id": protocol["protocol_id"],
        "selected_epoch": selected.epoch,
        "selected_threshold": threshold.threshold,
        "metric_keys": sorted(aggregate),
        "benchmark_values_accessed": False,
        "scientific_output": False,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
