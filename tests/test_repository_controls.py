from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts import validate_repository as validator


ROOT = Path(__file__).resolve().parents[1]


class RepositoryControlTests(unittest.TestCase):
    def test_repository_passes_all_control_checks(self) -> None:
        self.assertEqual([], validator.validate_repository(ROOT))

    def test_workflow_pins_checkout_to_full_sha(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        match = re.search(r"uses:\s*actions/checkout@([0-9a-f]{40})\b", workflow)
        self.assertIsNotNone(match)

    def test_invalid_json_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "broken.json").write_text("{", encoding="utf-8")
            errors = validator.check_json_documents(root)
        self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_cloud_sync_text_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = "One" + "Drive"
            (root / "config.txt").write_text(
                f"custody_root=C:/Users/example/{marker}/data", encoding="utf-8"
            )
            errors = validator.check_no_cloud_sync_references(root)
        self.assertTrue(any("operational cloud-sync" in error for error in errors))

    def test_explicit_cloud_sync_deny_policy_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = "One" + "Drive"
            (root / "AGENTS.md").write_text(
                f"Never write under C:/Users/example/{marker}.\n", encoding="utf-8"
            )
            (root / "control.json").write_text(
                json.dumps({"forbidden_roots": [f"C:/Users/example/{marker}"]}),
                encoding="utf-8",
            )
            self.assertEqual([], validator.check_no_cloud_sync_references(root))

    def test_model_artifact_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model_path = root / "model.pt"
            model_path.write_bytes(b"not-a-real-model")
            errors = validator.check_no_scientific_artifacts(root)
        self.assertTrue(any("artifact type" in error for error in errors))

    def test_artifact_gate_does_not_claim_model_authorized_future_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(
                json.dumps(
                    {"active_milestone_path": "records/milestones/MILESTONE-002.json"}
                ),
                encoding="utf-8",
            )
            (root / "model.pt").write_bytes(b"future-authorized-placeholder")
            self.assertEqual([], validator.check_no_scientific_artifacts(root))

    def test_milestone_one_rejects_model_and_array_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(
                json.dumps(
                    {
                        "active_milestone_path": (
                            "records/milestones/MILESTONE-001-PROVENANCE.json"
                        )
                    }
                ),
                encoding="utf-8",
            )
            (root / "model.pt").write_bytes(b"not-a-real-model")
            (root / "benchmark.npy").write_bytes(b"not-a-real-array")
            evaluation = root / "records" / "evaluations" / "result.json"
            evaluation.parent.mkdir(parents=True)
            evaluation.write_text("{}", encoding="utf-8")
            errors = validator.check_no_scientific_artifacts(root)
        self.assertTrue(any("model.pt" in error for error in errors))
        self.assertTrue(any("benchmark.npy" in error for error in errors))
        self.assertTrue(any("records/evaluations/result.json" in error for error in errors))
        self.assertTrue(all("milestone 1" in error for error in errors))

    def test_milestone_one_allows_provenance_readiness_and_intake_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(
                json.dumps(
                    {
                        "active_milestone_path": (
                            "records/milestones/MILESTONE-001-PROVENANCE.json"
                        )
                    }
                ),
                encoding="utf-8",
            )
            for directory in ("provenance", "readiness", "intake"):
                record = root / "records" / directory / "record.json"
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text("{}", encoding="utf-8")
            self.assertEqual([], validator.check_no_scientific_artifacts(root))

    def test_control_references_must_exist_and_point_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            milestone_path = root / validator.BOOTSTRAP_MILESTONE
            profile_path.parent.mkdir(parents=True)
            milestone_path.parent.mkdir(parents=True)
            profile_path.write_text(
                json.dumps(
                    {"active_milestone_path": validator.BOOTSTRAP_MILESTONE.as_posix()}
                ),
                encoding="utf-8",
            )
            milestone_path.write_text(
                json.dumps(
                    {"control_profile_path": validator.CONTROL_PROFILE.as_posix()}
                ),
                encoding="utf-8",
            )
            self.assertEqual([], validator.check_control_references(root))
            milestone_path.unlink()
            errors = validator.check_control_references(root)
        self.assertTrue(any("does not exist" in error for error in errors))

    def test_bootstrap_requires_explicit_zero_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            milestone_path = root / validator.BOOTSTRAP_MILESTONE
            profile_path.parent.mkdir(parents=True)
            milestone_path.parent.mkdir(parents=True)
            profile_path.write_text(
                json.dumps(
                    {
                        "active_milestone_path": validator.BOOTSTRAP_MILESTONE.as_posix(),
                        "scientific_state": "not_started",
                    }
                ),
                encoding="utf-8",
            )
            outputs = {field: 0 for field in validator.EMPTY_OUTPUT_FIELDS}
            milestone_path.write_text(
                json.dumps({"scientific_outputs": outputs}), encoding="utf-8"
            )
            self.assertEqual([], validator.check_truthful_bootstrap_state(root))
            outputs["training_runs"] = 1
            milestone_path.write_text(
                json.dumps({"scientific_outputs": outputs}), encoding="utf-8"
            )
            errors = validator.check_truthful_bootstrap_state(root)
        self.assertTrue(any("training_runs" in error for error in errors))

    def test_milestone_one_requires_zero_profile_and_contract_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            milestone_relative = Path(
                "records/milestones/MILESTONE-001-PROVENANCE.json"
            )
            milestone_path = root / milestone_relative
            profile_path.parent.mkdir(parents=True)
            milestone_path.parent.mkdir(parents=True)
            zero_outputs = {field: 0 for field in validator.EMPTY_OUTPUT_FIELDS}
            profile = {
                "active_milestone_path": milestone_relative.as_posix(),
                "scientific_state": "not_started",
                "scientific_outputs": dict(zero_outputs),
            }
            milestone = {"scientific_outputs": dict(zero_outputs)}
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            milestone_path.write_text(json.dumps(milestone), encoding="utf-8")
            self.assertEqual([], validator.check_truthful_bootstrap_state(root))

            for field in validator.MILESTONE_ONE_ZERO_OUTPUT_FIELDS:
                for location in ("profile", "milestone"):
                    with self.subTest(field=field, location=location):
                        candidate_profile = {
                            **profile,
                            "scientific_outputs": dict(zero_outputs),
                        }
                        candidate_milestone = {
                            "scientific_outputs": dict(zero_outputs)
                        }
                        candidate = (
                            candidate_profile
                            if location == "profile"
                            else candidate_milestone
                        )
                        candidate["scientific_outputs"][field] = 1
                        profile_path.write_text(
                            json.dumps(candidate_profile), encoding="utf-8"
                        )
                        milestone_path.write_text(
                            json.dumps(candidate_milestone), encoding="utf-8"
                        )
                        errors = validator.check_truthful_bootstrap_state(root)
                        self.assertTrue(
                            any(
                                f"{location} scientific_outputs.{field}" in error
                                for error in errors
                            )
                        )

    def test_milestone_one_dataset_admission_requires_completed_intake_records(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            milestone_relative = Path(
                "records/milestones/MILESTONE-001-PROVENANCE.json"
            )
            milestone_path = root / milestone_relative
            profile_path.parent.mkdir(parents=True)
            milestone_path.parent.mkdir(parents=True)
            outputs = {field: 0 for field in validator.EMPTY_OUTPUT_FIELDS}
            outputs["datasets"] = 1
            profile_path.write_text(
                json.dumps(
                    {
                        "active_milestone_path": milestone_relative.as_posix(),
                        "scientific_state": "not_started",
                        "scientific_outputs": outputs,
                    }
                ),
                encoding="utf-8",
            )
            milestone = {
                "scientific_outputs": dict(outputs),
                "units": [
                    {
                        "id": "M1-U005-CONTROLLED-BENCHMARK-INTAKE",
                        "status": "complete",
                        "disposition": "pass",
                    }
                ],
            }
            milestone_path.write_text(json.dumps(milestone), encoding="utf-8")
            errors = validator.check_truthful_bootstrap_state(root)
            self.assertTrue(any("record is missing" in error for error in errors))

            for relative in validator.MILESTONE_ONE_ADMISSION_RECORDS:
                record = root / relative
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text(
                    json.dumps({"record_id": relative.stem, "status": "pass"}),
                    encoding="utf-8",
                )
            self.assertEqual([], validator.check_truthful_bootstrap_state(root))

    def test_milestone_one_completed_zero_copy_requires_intake_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile_path = root / validator.CONTROL_PROFILE
            milestone_relative = Path(
                "records/milestones/MILESTONE-001-PROVENANCE.json"
            )
            milestone_path = root / milestone_relative
            profile_path.parent.mkdir(parents=True)
            milestone_path.parent.mkdir(parents=True)
            outputs = {field: 0 for field in validator.EMPTY_OUTPUT_FIELDS}
            profile_path.write_text(
                json.dumps(
                    {
                        "active_milestone_path": milestone_relative.as_posix(),
                        "scientific_state": "not_started",
                        "scientific_outputs": outputs,
                    }
                ),
                encoding="utf-8",
            )
            milestone_path.write_text(
                json.dumps(
                    {
                        "scientific_outputs": dict(outputs),
                        "units": [
                            {
                                "id": "M1-U005-CONTROLLED-BENCHMARK-INTAKE",
                                "status": "complete",
                                "disposition": "no_intake",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors = validator.check_truthful_bootstrap_state(root)
            self.assertEqual(
                2, sum("dataset admission record is missing" in error for error in errors)
            )

            for relative in validator.MILESTONE_ONE_ADMISSION_RECORDS:
                record = root / relative
                record.parent.mkdir(parents=True, exist_ok=True)
                record.write_text(
                    json.dumps(
                        {
                            "record_id": relative.stem,
                            "status": "no_intake",
                            "copied_files": [],
                        }
                    ),
                    encoding="utf-8",
                )
            self.assertEqual([], validator.check_truthful_bootstrap_state(root))


if __name__ == "__main__":
    unittest.main()
