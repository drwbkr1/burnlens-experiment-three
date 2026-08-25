from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    import numpy as np
    import torch
except ImportError:
    np = None
    torch = None


@unittest.skipIf(torch is None or np is None, "frozen training tests require approved runtime")
class FrozenTrainingTests(unittest.TestCase):
    def test_loader_rejects_test_before_filesystem_access(self) -> None:
        from burnlens_experiment_three.data import load_frozen_role

        with self.assertRaises(PermissionError):
            load_frozen_role(Path("does-not-exist"), {}, "test")

    def test_deterministic_npz_bytes(self) -> None:
        from burnlens_experiment_three.training import deterministic_npz

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            first = root / "first.npz"
            second = root / "second.npz"
            arrays = {"b": np.asarray([2.0], dtype="<f4"), "a": np.asarray([1.0], dtype="<f4")}
            deterministic_npz(first, arrays)
            deterministic_npz(second, arrays)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_frozen_optimizer_and_architecture_surface(self) -> None:
        from burnlens_experiment_three.model import FixedBurnChangeDetector, parameter_count

        model = FixedBurnChangeDetector()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0, amsgrad=False)
        self.assertEqual(137, parameter_count(model))
        self.assertEqual(0.001, optimizer.param_groups[0]["lr"])
        self.assertEqual((0.9, 0.999), optimizer.param_groups[0]["betas"])

    def test_training_checkpoint_uses_frozen_weights_filename(self) -> None:
        from burnlens_experiment_three.model import FixedBurnChangeDetector
        from burnlens_experiment_three.training import save_training_checkpoint

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            package = Path(temporary) / "checkpoint"
            manifest = save_training_checkpoint(FixedBurnChangeDetector(), package)
            self.assertEqual("weights.pt", manifest["weights_file"])
            self.assertTrue((package / "weights.pt").is_file())
            self.assertFalse((package / "state_dict.pt").exists())

    def test_runner_uses_frozen_replay_receipt_filenames(self) -> None:
        runner = (ROOT / "scripts/run_frozen_training.py").read_text(encoding="utf-8")
        verifier = (ROOT / "scripts/verify_frozen_training.py").read_text(
            encoding="utf-8"
        )
        for source in (runner, verifier):
            self.assertIn('"replay-receipt.json"', source)
            self.assertIn('"exact-replay-receipt.json"', source)
            self.assertNotIn('"fresh-process-reload.json"', source)
            self.assertNotIn('"run-receipt.json"', source)

    def test_runner_spawns_fresh_training_process_per_seed(self) -> None:
        runner = (ROOT / "scripts/run_frozen_training.py").read_text(encoding="utf-8")
        training = (ROOT / "src/burnlens_experiment_three/training.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('"--train-child"', runner)
        self.assertIn('"-I"', runner)
        self.assertIn('"fresh_isolated_subprocess_per_seed"', training)
        self.assertIn('"exception": None', training)


if __name__ == "__main__":
    unittest.main()
