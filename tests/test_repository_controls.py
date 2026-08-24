from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts import validate_repository as validator


ROOT = Path(__file__).resolve().parents[1]


class RepositoryControlTests(unittest.TestCase):
    def _write_completed_identity_fixture(
        self, root: Path, *, write_inventory: bool = True
    ) -> tuple[dict[str, object], Path, dict[str, object], Path]:
        profile_path = root / validator.CONTROL_PROFILE
        milestone_path = root / validator.PROVENANCE_MILESTONE
        inventory_path = root / validator.PROVENANCE_IDENTITY_INVENTORY
        profile_path.parent.mkdir(parents=True)
        milestone_path.parent.mkdir(parents=True)
        profile_path.write_text(
            json.dumps(
                {
                    "active_milestone_path": (
                        validator.PROVENANCE_MILESTONE.as_posix()
                    )
                }
            ),
            encoding="utf-8",
        )
        expected_gates = {
            "source_repository_read_only": "pass",
            "exact_git_and_path_identity": "pass",
            "sha256_every_candidate": "pass",
            "role_and_exposure_classification": "pass",
            "missing_rejected_ambiguous_retained": "pass",
        }
        milestone: dict[str, object] = {
            "units": [
                {
                    "id": "M1-U002-READ-ONLY-IDENTITY-INVENTORY",
                    "status": "complete",
                    "disposition": "pass",
                    "outputs": [validator.PROVENANCE_IDENTITY_INVENTORY.as_posix()],
                    "gates": expected_gates,
                    "exit_condition_delta": {
                        "expected": ["EXIT-M1-IDENTITY"],
                        "observed": ["EXIT-M1-IDENTITY"],
                        "decision_value": "advances_exit",
                    },
                }
            ],
            "exit_conditions": [
                {
                    "id": "EXIT-M1-IDENTITY",
                    "status": "pass",
                    "evidence": [
                        validator.PROVENANCE_IDENTITY_INVENTORY.as_posix()
                    ],
                }
            ],
        }
        milestone_path.write_text(
            json.dumps(milestone, indent=2), encoding="utf-8"
        )
        inventory = json.loads(
            (ROOT / validator.PROVENANCE_IDENTITY_INVENTORY).read_text(
                encoding="utf-8"
            )
        )
        if write_inventory:
            inventory_path.parent.mkdir(parents=True)
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
        return inventory, inventory_path, milestone, milestone_path

    def test_repository_passes_all_control_checks(self) -> None:
        self.assertEqual([], validator.validate_repository(ROOT))

    def test_completed_u002_inventory_is_self_consistent_without_source_access(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_completed_identity_fixture(root)
            self.assertEqual(
                [], validator.check_milestone_one_identity_inventory(root)
            )

    def test_completed_u002_requires_a_nonempty_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, inventory_path, _, _ = self._write_completed_identity_fixture(
                root, write_inventory=False
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(any("inventory is missing" in error for error in errors))

            inventory_path.parent.mkdir(parents=True)
            inventory_path.write_text("", encoding="utf-8")
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(any("must be non-empty" in error for error in errors))

    def test_completed_u002_recomputes_dataset_and_unet_rosters(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory, inventory_path, _, _ = self._write_completed_identity_fixture(
                root
            )
            dataset_row = inventory["dataset"]["arrays"][0]
            dataset_row["observed_sha256"] = "0" * 64
            dataset_row["expected_sha256"] = "0" * 64
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(
                any("dataset array roster SHA-256" in error for error in errors)
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory, inventory_path, _, _ = self._write_completed_identity_fixture(
                root
            )
            prediction = inventory["comparison_artifacts"]["canonical_unet"][
                "predictions"
            ][0]
            prediction["observed_sha256"] = "0" * 64
            prediction["expected_sha256"] = "0" * 64
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(
                any("U-Net prediction roster SHA-256" in error for error in errors)
            )

    def test_completed_u002_enforces_binding_counts_and_source_roster(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory, inventory_path, _, _ = self._write_completed_identity_fixture(
                root
            )
            inventory["source_and_terms_evidence"]["direct_bindings"][
                "proposals"
            ].pop()
            inventory["source_and_terms_evidence"][
                "supplemental_transitive_chain"
            ].pop()
            inventory["source_and_terms_evidence"]["source_terms_roster"][
                "aggregate_bytes"
            ] = 0
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(
                any(
                    "direct bindings proposals must contain exactly 5" in error
                    for error in errors
                )
            )
            self.assertTrue(
                any(
                    "supplemental transitive records must contain exactly 5" in error
                    for error in errors
                )
            )
            self.assertTrue(
                any("source_terms_roster.aggregate_bytes" in error for error in errors)
            )

    def test_completed_u002_enforces_boundaries_and_exit_consistency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory, inventory_path, milestone, milestone_path = (
                self._write_completed_identity_fixture(root)
            )
            inventory["lane_dispositions"]["controlled_local_copy"] = "PASS"
            inventory["lane_dispositions"]["bytes_copied"] = 1
            inventory["scientific_outputs_created"]["evaluations"] = 1
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
            milestone["units"][0]["gates"]["sha256_every_candidate"] = "fail"
            milestone["exit_conditions"][0]["status"] = "pending"
            milestone_path.write_text(
                json.dumps(milestone, indent=2), encoding="utf-8"
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(
                any("controlled_local_copy must equal DEFER" in error for error in errors)
            )
            self.assertTrue(any("bytes_copied must equal 0" in error for error in errors))
            self.assertTrue(
                any("scientific_outputs_created.evaluations" in error for error in errors)
            )
            self.assertTrue(
                any("gates.sha256_every_candidate" in error for error in errors)
            )
            self.assertTrue(
                any("EXIT-M1-IDENTITY status must be 'pass'" in error for error in errors)
            )

    def test_completed_u002_binds_exact_experiment_one_git_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory, inventory_path, _, _ = self._write_completed_identity_fixture(
                root
            )
            inventory["source_repository"]["tree"] = "0" * 40
            inventory_path.write_text(
                json.dumps(inventory, indent=2), encoding="utf-8"
            )
            errors = validator.check_milestone_one_identity_inventory(root)
            self.assertTrue(
                any("source_repository.tree" in error for error in errors)
            )

    def test_prepared_owner_rights_review_remains_exact_and_blank(self) -> None:
        self.assertEqual([], validator.check_owner_rights_review_preparation(ROOT))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = (
                validator.PROVENANCE_MILESTONE,
                validator.OWNER_RIGHTS_REVIEW_ITEM,
                validator.OWNER_RIGHTS_REVIEW_CONTRACT,
                validator.OWNER_RIGHTS_BLANK_RESPONSE,
            )
            for relative in paths:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())

            blank_path = root / validator.OWNER_RIGHTS_BLANK_RESPONSE
            blank = json.loads(blank_path.read_text(encoding="utf-8"))
            blank["responses"][0]["decision"] = "yes"
            blank_path.write_text(json.dumps(blank, indent=2) + "\n", encoding="utf-8")

            errors = validator.check_owner_rights_review_preparation(root)
            self.assertTrue(any("file hash changed" in error for error in errors))
            self.assertTrue(any("zero decisions" in error for error in errors))

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
