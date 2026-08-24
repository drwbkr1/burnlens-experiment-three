from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

try:
    import torch
except ImportError:  # CI's bootstrap runtime intentionally has no neural dependency.
    torch = None


@unittest.skipIf(torch is None, "synthetic neural tests require the approved runtime")
class SyntheticNeuralLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        from burnlens_experiment_three.model import FixedBurnChangeDetector

        torch.use_deterministic_algorithms(True)
        torch.manual_seed(20260725)
        self.model = FixedBurnChangeDetector()

    def test_fixed_architecture_has_exactly_137_parameters(self) -> None:
        from burnlens_experiment_three.model import parameter_count

        self.assertEqual(137, parameter_count(self.model))
        convolutions = [module for module in self.model.modules() if isinstance(module, torch.nn.Conv2d)]
        self.assertEqual([(6, 8), (8, 8), (8, 1)], [(layer.in_channels, layer.out_channels) for layer in convolutions])
        self.assertTrue(all(layer.kernel_size == (1, 1) for layer in convolutions))

    def test_forward_accepts_arbitrary_spatial_dimensions(self) -> None:
        for height, width in ((8, 11), (32, 32), (7, 19)):
            with self.subTest(height=height, width=width):
                output = self.model(torch.zeros((2, 6, height, width), dtype=torch.float32))
                self.assertEqual((2, 1, height, width), tuple(output.shape))

    def test_loss_balances_events_and_present_classes(self) -> None:
        from burnlens_experiment_three.losses import event_class_balanced_masked_bce

        logits = torch.tensor([[[[-2.0, 2.0]]], [[[1.0, -1.0]]]])
        targets = torch.tensor([[[[0.0, 1.0]]], [[[0.0, 1.0]]]])
        mask = torch.ones_like(targets, dtype=torch.bool)
        events = torch.tensor([0, 1])
        observed = event_class_balanced_masked_bce(logits, targets, mask, events)
        event_zero = torch.nn.functional.binary_cross_entropy_with_logits(logits[0], targets[0])
        event_one = torch.nn.functional.binary_cross_entropy_with_logits(logits[1], targets[1])
        self.assertTrue(torch.equal(observed, (event_zero + event_one) / 2.0))

    def test_masked_unknowns_do_not_become_background(self) -> None:
        from burnlens_experiment_three.losses import event_class_balanced_masked_bce

        logits_a = torch.tensor([[[[-1.0, 99.0, 1.0]]]])
        logits_b = torch.tensor([[[[-1.0, -99.0, 1.0]]]])
        targets = torch.tensor([[[[0.0, 0.0, 1.0]]]])
        mask = torch.tensor([[[[True, False, True]]]])
        events = torch.tensor([0])
        loss_a = event_class_balanced_masked_bce(logits_a, targets, mask, events)
        loss_b = event_class_balanced_masked_bce(logits_b, targets, mask, events)
        self.assertTrue(torch.equal(loss_a, loss_b))

    def test_state_dict_package_reloads_exactly_and_rejects_hash_drift(self) -> None:
        from burnlens_experiment_three.checkpoint import (
            load_state_dict_package,
            save_state_dict_package,
            tensor_state_sha256,
        )
        from burnlens_experiment_three.model import FixedBurnChangeDetector

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            package = Path(temporary) / "package"
            manifest = save_state_dict_package(self.model, package)
            reloaded = FixedBurnChangeDetector()
            load_state_dict_package(reloaded, package)
            self.assertEqual(manifest["tensor_state_sha256"], tensor_state_sha256(reloaded.state_dict()))
            parsed = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
            parsed["weights_sha256"] = "0" * 64
            (package / "manifest.json").write_text(json.dumps(parsed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checkpoint file hash mismatch"):
                load_state_dict_package(reloaded, package)

    def test_synthetic_fixture_is_deterministic_and_contains_two_events(self) -> None:
        from burnlens_experiment_three.synthetic import make_synthetic_batch

        first = make_synthetic_batch()
        second = make_synthetic_batch()
        self.assertTrue(torch.equal(first.inputs, second.inputs))
        self.assertTrue(torch.equal(first.targets, second.targets))
        self.assertEqual([0, 0, 1, 1], first.event_ids.tolist())
        self.assertTrue(torch.any(first.targets == 0.0))
        self.assertTrue(torch.any(first.targets == 1.0))
        self.assertTrue(torch.any(~first.loss_mask))


if __name__ == "__main__":
    unittest.main()
