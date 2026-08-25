from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

try:
    import numpy as np
    import torch  # noqa: F401
    import rasterio  # noqa: F401
    from PIL import Image  # noqa: F401
    HAS_APPROVED_RUNTIME = True
except ModuleNotFoundError:  # system Python control run
    np = None
    HAS_APPROVED_RUNTIME = False

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@unittest.skipIf(not HAS_APPROVED_RUNTIME, "evaluation tests require approved runtime")
class RetrospectiveEvaluationTests(unittest.TestCase):
    def test_real_controller_marks_opening_before_test_deserialization(self) -> None:
        source = (ROOT / "scripts/run_retrospective_evaluation.py").read_text(encoding="utf-8")
        self.assertLess(source.index("marker = create_opening_root"), source.index("data = load_opened_test"))
        self.assertLess(source.index("data = load_opened_test"), source.index("unet_prediction, unet_probability = load_unet_comparator"))
        self.assertIn('EXPECTED_OUTPUT_NAME = "m5-2026-001"', source)
        self.assertIn("exist_ok=False", (ROOT / "src/burnlens_experiment_three/evaluation.py").read_text(encoding="utf-8"))

    def test_opening_root_is_exclusive_and_marker_is_first(self) -> None:
        from burnlens_experiment_three.evaluation import create_opening_root
        with tempfile.TemporaryDirectory(dir=Path(r"C:\Projects\Active")) as temporary:
            root = Path(temporary) / "evaluation"
            marker = create_opening_root(root, {"state": "opening", "values_decoded": 0})
            self.assertEqual({"state": "opening", "values_decoded": 0}, json.loads(marker.read_text()))
            with self.assertRaises(FileExistsError):
                create_opening_root(root, {"state": "second-opening"})

    def test_metrics_preserve_events_classes_and_nonconstant_gate(self) -> None:
        from burnlens_experiment_three.evaluation import evaluate_predictions
        truth = np.array([[[0, 1]], [[1, 0]], [[0, 1]], [[1, 0]]], dtype=np.uint8)
        prediction = np.array([[[0, 1]], [[1, 0]], [[1, 0]], [[1, 0]]], dtype=np.uint8)
        mask = np.ones_like(truth, dtype=bool)
        result = evaluate_predictions(truth, prediction, mask, ["a", "a", "b", "b"])
        self.assertEqual(8, result["aggregate"]["eligible_pixels"])
        self.assertTrue(result["aggregate"]["all_events_nonconstant"])
        self.assertEqual({"0", "1"}, set(result["events"][0]["classes"]))

    def test_comparative_rule_requires_nonconstant_and_strict_both(self) -> None:
        from burnlens_experiment_three.evaluation import comparative_disposition
        seeds = [{"aggregate": {"event_class_macro_iou": 0.7, "worst_event_macro_dice": 0.7, "all_events_nonconstant": True}} for _ in range(3)]
        constants = [{"aggregate": {"event_class_macro_iou": 0.3, "worst_event_macro_dice": 0.3}}, {"aggregate": {"event_class_macro_iou": 0.4, "worst_event_macro_dice": 0.4}}]
        self.assertEqual("PASS", comparative_disposition(seeds, constants)["comparative_status"])
        seeds[0]["aggregate"]["all_events_nonconstant"] = False
        self.assertEqual("FAIL", comparative_disposition(seeds, constants)["comparative_status"])

    def test_rbr_formula_matches_frozen_definition(self) -> None:
        from burnlens_experiment_three.evaluation import rbr_probability_score
        features = np.zeros((1, 6, 1, 1), dtype=np.float32)
        features[:, 1] = 0.75; features[:, 2] = 0.25
        features[:, 4] = 0.45; features[:, 5] = 0.55
        self.assertAlmostEqual(0.6 / 1.501, float(rbr_probability_score(features)[0, 0, 0]), places=6)


if __name__ == "__main__":
    unittest.main()
