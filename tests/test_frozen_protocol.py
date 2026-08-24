from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "burnlens_experiment_three"))

from metrics import aggregate_events, event_metrics, three_seed_median
from protocol import load_protocol, validate_protocol
from selection import (
    EpochObservation,
    ThresholdScore,
    early_stop_epoch,
    select_checkpoint,
    select_shared_threshold,
    threshold_grid,
)


class FrozenProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = ROOT / "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
        self.protocol = load_protocol(self.path)

    def test_exact_fixed_values_and_role_isolation(self) -> None:
        self.assertEqual(137, self.protocol["model"]["trainable_parameters"])
        self.assertEqual([20260725, 20260726, 20260727], self.protocol["execution"]["seeds"])
        roles = self.protocol["data"]["roles"]
        events = [set(value["event_group_ids"]) for value in roles.values()]
        self.assertTrue(events[0].isdisjoint(events[1]))
        self.assertTrue(events[0].isdisjoint(events[2]))
        self.assertTrue(events[1].isdisjoint(events[2]))

    def test_protocol_rejects_scientific_drift(self) -> None:
        changed = json.loads(json.dumps(self.protocol))
        changed["execution"]["optimizer"]["learning_rate"] = 0.01
        with self.assertRaisesRegex(ValueError, "optimizer drift"):
            validate_protocol(changed)

    def test_checkpoint_selection_uses_minimum_then_earliest(self) -> None:
        selected = select_checkpoint(
            [EpochObservation(1, 0.7), EpochObservation(2, 0.6), EpochObservation(3, 0.6)]
        )
        self.assertEqual(2, selected.epoch)

    def test_early_stop_requires_exactly_25_stale_epochs(self) -> None:
        rows = [EpochObservation(1, 0.5)] + [EpochObservation(index, 0.5) for index in range(2, 27)]
        self.assertEqual(26, early_stop_epoch(rows))
        self.assertIsNone(early_stop_epoch(rows[:-1]))

    def test_threshold_grid_and_all_ties_are_deterministic(self) -> None:
        self.assertEqual(99, len(threshold_grid()))
        scores = [ThresholdScore(value, 0.5, 0.5) for value in threshold_grid()]
        self.assertEqual(0.5, select_shared_threshold(scores).threshold)
        scores = [ThresholdScore(value, 0.5, 0.5) for value in threshold_grid()]
        scores[48] = ThresholdScore(0.49, 0.7, 0.7)
        scores[50] = ThresholdScore(0.51, 0.7, 0.7)
        self.assertEqual(0.49, select_shared_threshold(scores).threshold)

    def test_binary_metrics_and_nonconstant_gate(self) -> None:
        perfect = event_metrics([0, 1], [0, 1])
        constant = event_metrics([0, 1], [1, 1])
        self.assertTrue(perfect["nonconstant"])
        self.assertFalse(constant["nonconstant"])
        aggregate = aggregate_events([perfect, constant])
        self.assertAlmostEqual(0.625, aggregate["event_class_macro_iou"])
        self.assertEqual(0.5, three_seed_median([0.1, 0.5, 0.9]))

    def test_claim_and_test_opening_boundaries_are_explicit(self) -> None:
        self.assertIn("statistical significance or superiority", self.protocol["claim_envelope"]["prohibited"])
        self.assertIn("one controlled opening", self.protocol["data"]["roles"]["test"]["opening_policy"])
        self.assertIn("Experiment 3B", self.protocol["exception_policy"]["after_test_opening"])


if __name__ == "__main__":
    unittest.main()
