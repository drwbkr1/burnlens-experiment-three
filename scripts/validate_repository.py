#!/usr/bin/env python3
"""Validate the repository control plane without third-party dependencies."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]

HISTORICAL_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-001.json"
)
MILESTONE_ONE_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-002.json"
)
MILESTONE_TWO_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-003.json"
)
MILESTONE_THREE_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-004.json"
)
MILESTONE_FOUR_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-005.json"
)
MILESTONE_FIVE_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-006.json"
)
MILESTONE_SIX_CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-007.json"
)
MILESTONE_SIX_RELEASE_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-008.json"
)
CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-009.json"
)
BOOTSTRAP_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-000-BOOTSTRAP-2026-001.json"
)
PROVENANCE_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-001-PROVENANCE-2026-001.json"
)
SYNTHETIC_PREFLIGHT_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-002-SYNTHETIC-PREFLIGHT-2026-001.json"
)
PROTOCOL_FREEZE_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-003-PROTOCOL-FREEZE-2026-001.json"
)
FROZEN_TRAINING_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-004-FROZEN-TRAINING-2026-001.json"
)
RETROSPECTIVE_EVALUATION_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-005-RETROSPECTIVE-EVALUATION-2026-001.json"
)
TERMINAL_RELEASE_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-006-RELEASE-CLOSEOUT-2026-001.json"
)
PREOPENING_AUDIT = Path(
    "records/evaluation/EXPERIMENT-THREE-M5-PREOPENING-AUDIT-2026-001.json"
)
PREOPENING_VERIFIER = Path("scripts/verify_preopening_audit.py")
EVALUATION_PATH_PREFLIGHT = Path(
    "records/evaluation/EXPERIMENT-THREE-M5-EVALUATION-PATH-PREFLIGHT-2026-001.json"
)
RETROSPECTIVE_EVALUATION_RECORD = Path(
    "records/evaluation/EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json"
)
PUBLIC_EVIDENCE_MANIFEST = Path(
    "records/release/EXPERIMENT-THREE-PUBLIC-EVIDENCE-MANIFEST-2026-001.json"
)
REVIEWER_EVIDENCE_RECORD = Path(
    "records/release/EXPERIMENT-THREE-M6-REVIEWER-EVIDENCE-2026-001.json"
)
REVIEWER_RENDERER = Path("scripts/render_reviewer_evidence.py")
RELEASE_SURFACE_MATRIX = Path(
    "records/release/EXPERIMENT-THREE-M6-REAL-SURFACE-MATRIX-2026-001.json"
)
RELEASE_AUDIT = Path(
    "records/release/EXPERIMENT-THREE-M6-RELEASE-AUDIT-2026-001.json"
)
RELEASE_CANDIDATE = Path(
    "records/release/EXPERIMENT-THREE-M6-RELEASE-CANDIDATE-2026-001.json"
)
LIVE_RELEASE_RECORD = Path(
    "records/release/EXPERIMENT-THREE-M6-LIVE-RELEASE-VERIFICATION-2026-001.json"
)
LIVE_RELEASE_SURFACE_MATRIX = Path(
    "records/release/EXPERIMENT-THREE-M6-REAL-SURFACE-MATRIX-2026-002.json"
)
LIVE_RELEASE_AUDIT = Path(
    "records/release/EXPERIMENT-THREE-M6-RELEASE-AUDIT-2026-002.json"
)
TERMINAL_CLOSEOUT_RECORD = Path(
    "records/release/EXPERIMENT-THREE-TERMINAL-CLOSEOUT-2026-001.json"
)
EVALUATION_PATH_SOURCES = {
    Path("src/burnlens_experiment_three/evaluation.py"): "3c375ecd4e3983bb28e8193a2a479be948cf270e5332f13e938661dd0320a812",
    Path("scripts/run_evaluation_path_preflight.py"): "dbe6a1089fe4c5f4c849492ea8ccc1925b24d5ee766430e74b497a7130f0dd94",
    Path("scripts/run_retrospective_evaluation.py"): "6d09f0b1dcf9ef12fe078488d6c980d0154ae86e0cf45145ac9c4b68e26c0045",
    Path("scripts/verify_retrospective_evaluation.py"): "9fccb4b6a28adbd17ea65e3c2e2522b3721e14de74784c4fb6105f1fc11f9337",
    Path("tests/test_retrospective_evaluation.py"): "3ac5f4208d40a4fee315d00ea17f3fdd6e3b46d429ee6596f72576fec4964282",
}
STATE_RECONCILIATION = Path(
    "records/reconciliations/EXPERIMENT-THREE-STATE-2026-001.json"
)
PROVENANCE_IDENTITY_INVENTORY = Path(
    "records/provenance/"
    "EXPERIMENT-ONE-BENCHMARK-IDENTITY-INVENTORY-2026-001.json"
)

EXPECTED_PROVENANCE_INVENTORY_ID = (
    "EXPERIMENT-ONE-BENCHMARK-IDENTITY-INVENTORY-2026-001"
)
EXPECTED_EXPERIMENT_ONE_HEAD = "a741111d82e69689022d2058118ed8f4b9bf3546"
EXPECTED_EXPERIMENT_ONE_TREE = "bc679254030eb57a65f58ac2af10880866fc52be"
EXPECTED_DATASET_ROSTER_SHA256 = (
    "5f186ccd240db26483195421701baf83b7e85436e92a851ace638c249d0b43dd"
)
EXPECTED_SOURCE_TERMS_ROSTER_SHA256 = (
    "953b428175b01a6392b957651b08ad8376bda698d5b679fbe3b07f18a0845702"
)
EXPECTED_UNET_PREDICTION_ROSTER_SHA256 = (
    "665510bb89920bf192a6342d0a968613ecc4d01998bd374fa5cfc19c0a7c8dfb"
)
OWNER_RIGHTS_REVIEW_ITEM = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-ONE-ARTIFACT-RIGHTS-REVIEW-ITEM-2026-001.json"
)
OWNER_RIGHTS_REVIEW_CONTRACT = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-ONE-ARTIFACT-RIGHTS-REVIEW-CONTRACT-2026-001.json"
)
OWNER_RIGHTS_BLANK_RESPONSE = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-ONE-ARTIFACT-RIGHTS-RESPONSE-BLANK-2026-001.json"
)
EXPECTED_OWNER_REVIEW_ID = "EXPERIMENT-ONE-ARTIFACT-RIGHTS-REVIEW-2026-001"
EXPECTED_OWNER_REVIEW_ITEM_ID = "experiment-one-project-authored-derivative-artifacts"
EXPECTED_OWNER_REVIEW_ITEM_SHA256 = (
    "2454921e3ed2cd5d786bb1599fb94c06c0c9ac3ae2010a021667830fe72a5581"
)
EXPECTED_OWNER_REVIEW_CONTRACT_SHA256 = (
    "0be9b7f10037cc67c3747778b4751ed4e4e7348d9d219e95d997094b06726ac3"
)
EXPECTED_OWNER_RIGHTS_BLANK_SHA256 = (
    "3abf9c707da4c96657898fc20dbd01723daa01fca0f8779412d009e5d06b080e"
)
OWNER_RIGHTS_DECISION = Path(
    "records/decisions/EXPERIMENT-ONE-ARTIFACT-RIGHTS-DECISION-2026-001.json"
)
SOURCE_GATE = Path(
    "records/source-gates/EXPERIMENT-ONE-BENCHMARK-SOURCE-GATE-2026-001.json"
)
READINESS_INPUT = Path(
    "records/readiness/EXPERIMENT-ONE-BENCHMARK-READINESS-2026-001.json"
)
READINESS_DECISION = Path(
    "records/readiness/EXPERIMENT-ONE-BENCHMARK-READINESS-DECISION-2026-001.json"
)
ADMISSION_MANIFEST = Path(
    "records/intake/EXPERIMENT-ONE-BENCHMARK-ADMISSION-MANIFEST-2026-001.json"
)
INTAKE_RECEIPT = Path(
    "records/intake/EXPERIMENT-ONE-BENCHMARK-INTAKE-RECEIPT-2026-001.json"
)
EXPECTED_OWNER_RIGHTS_DECISION_SHA256 = (
    "ce7efbbf6eb70713211f46228ffdd6b98fdd5d154afab91fdd75fa1cd887e1bf"
)
EXPECTED_SOURCE_GATE_SHA256 = (
    "cd54bc87af84785c59f6018307d84d8ad4ebf49b9f6270e90543b9d2bada5de5"
)
EXPECTED_READINESS_INPUT_SHA256 = (
    "61f8afe7952d9b6ec30db5cbcb61af25830941f763aa45286e65e88d29079ce3"
)
EXPECTED_READINESS_DECISION_SHA256 = (
    "8fa1d50a4e02bcd2545421569cc78fe28203ad1647e274d6ec23805e45272cb7"
)
EXPECTED_ADMISSION_MANIFEST_SHA256 = (
    "159c79d4394df73db2817cb8e7659e13501158c9f1f2d9152fc8d396bf3781ea"
)
EXPECTED_INTAKE_RECEIPT_SHA256 = (
    "6734472a7891078b6916c1b9ceba891214616f7670261348fcb7e81c93126c76"
)
EXPECTED_INTAKE_ASSET_COUNT = 131
EXPECTED_INTAKE_BYTES = 3_369_748
EXPECTED_INTAKE_ROSTER_SHA256 = (
    "0daf93b2b3a21330d501c9e222d907738c19e4d5b9e00ebbdd169b65aadb89f4"
)
RUNTIME_INVENTORY = Path(
    "records/runtime/EXPERIMENT-THREE-RUNTIME-CANDIDATE-INVENTORY-2026-001.json"
)
RUNTIME_SOURCE_GATE = Path(
    "records/source-gates/EXPERIMENT-THREE-RUNTIME-SOURCE-GATE-2026-001.json"
)
RUNTIME_REVIEW_ITEM = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-THREE-RUNTIME-ADOPTION-REVIEW-ITEM-2026-001.json"
)
RUNTIME_REVIEW_CONTRACT = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-THREE-RUNTIME-ADOPTION-REVIEW-CONTRACT-2026-001.json"
)
RUNTIME_BLANK_RESPONSE = Path(
    "records/decisions/reviews/"
    "EXPERIMENT-THREE-RUNTIME-ADOPTION-RESPONSE-BLANK-2026-001.json"
)
RUNTIME_ADOPTION_DECISION = Path(
    "records/decisions/EXPERIMENT-THREE-RUNTIME-ADOPTION-DECISION-2026-001.json"
)
EXPECTED_RUNTIME_REVIEW_ID = "EXPERIMENT-THREE-RUNTIME-ADOPTION-REVIEW-2026-001"
EXPECTED_RUNTIME_ITEM_ID = "exact-windows-cpu-runtime-candidate-001"
EXPECTED_RUNTIME_INVENTORY_SHA256 = (
    "68f34338b61da111e0fc20a9a2a02cca7e02ff97262fd5f9d0185d351fc69f05"
)
EXPECTED_RUNTIME_SOURCE_GATE_SHA256 = (
    "1db59fb03c55051ce50a7327f45f7f9515eefce0dd7035640a07e35eb34f6e47"
)
EXPECTED_RUNTIME_ITEM_SHA256 = (
    "e0af6dcd8dcca8d945ed82fe9df9ab12792e89c70e0ce44d531dfa8b2add998d"
)
EXPECTED_RUNTIME_CONTRACT_SHA256 = (
    "b0743b466904a2580c90d4df7b8806e70eae1535a1702e14e6245eb30bbb18ce"
)
EXPECTED_RUNTIME_BLANK_SHA256 = (
    "45363c2a1d29200dab289031f9cfbd7a5811f4615f3a33a40629f05b2e37f039"
)
EXPECTED_RUNTIME_DECISION_SHA256 = (
    "af559ec1ebeebea5338b5c8e8b0200dbb98026980111de56fbbfd4f364a8b4ee"
)
RUNTIME_ACTIVATION_FAILURE = Path(
    "records/runtime/EXPERIMENT-THREE-RUNTIME-ACTIVATION-FAILURE-2026-001.json"
)
RUNTIME_SUCCESSOR_INVENTORY = Path(
    "records/runtime/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-CANDIDATE-INVENTORY-2026-001.json"
)
RUNTIME_SUCCESSOR_SOURCE_GATE = Path(
    "records/source-gates/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-SOURCE-GATE-2026-001.json"
)
RUNTIME_SUCCESSOR_REVIEW_ITEM = Path(
    "records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ADOPTION-REVIEW-ITEM-2026-001.json"
)
RUNTIME_SUCCESSOR_REVIEW_CONTRACT = Path(
    "records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ADOPTION-REVIEW-CONTRACT-2026-001.json"
)
RUNTIME_SUCCESSOR_BLANK_RESPONSE = Path(
    "records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ADOPTION-RESPONSE-BLANK-2026-001.json"
)
RUNTIME_SUCCESSOR_ADOPTION_DECISION = Path(
    "records/decisions/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ADOPTION-DECISION-2026-001.json"
)
RUNTIME_SUCCESSOR_ACTIVATION = Path(
    "records/runtime/EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ACTIVATION-2026-001.json"
)
EXPECTED_RUNTIME_FAILURE_SHA256 = (
    "a6f98a20371a1ee3a6ad36e7d272fc21fa952d41bf6a5fa9c6abdf28ed803512"
)
EXPECTED_RUNTIME_SUCCESSOR_INVENTORY_SHA256 = (
    "ae95bc3982766e996c0ec6cb15d4964738f1958f48b1eabe73d2e2d27b3e3967"
)
EXPECTED_RUNTIME_SUCCESSOR_SOURCE_GATE_SHA256 = (
    "e8dcd17e040c846459090c42037b51e333f8d285286f8c94467c2ff62e9c42b3"
)
EXPECTED_RUNTIME_SUCCESSOR_ITEM_SHA256 = (
    "f010073113c7268ba75c35a37dc5cded51c954af05f04fdb7f28d15c5175b615"
)
EXPECTED_RUNTIME_SUCCESSOR_CONTRACT_SHA256 = (
    "bf50874168e2024f953f8748435f46f0b2554ca5beeff9ec701f5ce032f28d39"
)
EXPECTED_RUNTIME_SUCCESSOR_BLANK_SHA256 = (
    "0e7b117acbfe1cf9517e1a05e2cf0bae39524123efea2b5907321196ba9b796b"
)
EXPECTED_RUNTIME_SUCCESSOR_DECISION_SHA256 = (
    "0bb8daafca4198b995f09952404fd93d185e4dccccb0ed45fc072143d491a29e"
)
EXPECTED_RUNTIME_SUCCESSOR_ACTIVATION_SHA256 = (
    "991d843e0dcfae6a2568fd837389d4ee5b64e36f1077f8299399a4f37e21083a"
)
EXPECTED_RUNTIME_SUCCESSOR_REVIEW_ID = (
    "EXPERIMENT-THREE-RUNTIME-SUCCESSOR-ADOPTION-REVIEW-2026-001"
)
EXPECTED_RUNTIME_SUCCESSOR_ITEM_ID = "exact-windows-cpu-runtime-successor-002"
SYNTHETIC_PREFLIGHT_RECORD = Path(
    "records/synthetic/EXPERIMENT-THREE-SYNTHETIC-PREFLIGHT-2026-001.json"
)
SYNTHETIC_SOURCE_IDENTITIES = {
    Path("src/burnlens_experiment_three/__init__.py"): "7f51f0ead6abda4b9c7b18e6b65371e06de7ca069cfdd5173fa4cbc6e371a5eb",
    Path("src/burnlens_experiment_three/model.py"): "f7e68601c4d00d11a6569ee1f870815b7a0f16f7e1b1a116dbcd936312665313",
    Path("src/burnlens_experiment_three/losses.py"): "aec40aae4e98042d5f73d59baeed3948c8073b18ed131f2c0e263749b5ed60a9",
    Path("src/burnlens_experiment_three/synthetic.py"): "baa3640ff1db93f098a419f8b55fb2258d6ceccd714e441cd1a6373bca6955a6",
    Path("src/burnlens_experiment_three/checkpoint.py"): "529870f28236592472d363a085ba9bf0a47c247af322fc114c57b515927805f8",
    Path("scripts/run_synthetic_preflight.py"): "044946c5ddbc13dc023434ccf0faa0428921c9c5b3a722134fa274b4d01ca351",
    Path("scripts/verify_synthetic_preflight.py"): "a79be6988b69149e0680aca9d92fe64f20d9e63b06918506caa25790f3bfefbf",
    Path("tests/test_synthetic_neural_lifecycle.py"): "92ddf8e89b599d2f447a0d74444789b7c09532e6973bc1cad5c39dcf2f6feb4c",
}
EXPECTED_SYNTHETIC_PREFLIGHT_RECORD_SHA256 = (
    "88fa5c37134c2f91b74d9435cb353ab57664384ef19536b7984f89cccf487c10"
)
FROZEN_PROTOCOL = Path(
    "protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"
)
PROTOCOL_FREEZE_RECORD = Path(
    "records/protocol/EXPERIMENT-THREE-PROTOCOL-FREEZE-2026-001.json"
)
EXPECTED_FROZEN_PROTOCOL_SHA256 = (
    "12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e"
)
EXPECTED_PROTOCOL_FREEZE_RECORD_SHA256 = (
    "3be942adeda2957f6f0ee9556d605369d3b213e95b43aeab7321f2906449707f"
)
TRAIN_VALIDATION_DATA_RECORD = Path(
    "records/training/EXPERIMENT-THREE-M4-TRAIN-VALIDATION-DATA-2026-001.json"
)
FROZEN_TRAINING_RECORD = Path(
    "records/training/EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001.json"
)
FROZEN_TRAINING_SOURCE_IDENTITIES = {
    Path("src/burnlens_experiment_three/data.py"): "36147290692689e45373125cda8eadba9c8a7894b72716c8b3b21061e746946d",
    Path("src/burnlens_experiment_three/training.py"): "a68cb3749895d7c177549d26a966fbfd17e619b967c3614741d4fe893ac1ef1e",
    Path("scripts/run_frozen_training.py"): "8c1d43b8dffaa616c7c0925693292d2501ec6365e546a486fb59bbc275152b0d",
    Path("scripts/verify_frozen_training.py"): "494a8f9dc5197451da9bc5cff11a6621db0a1dcd84456fc39eb17859aa009781",
    Path("scripts/verify_train_validation_data.py"): "5fadbfdd91b40bc3e1dfe026ae04857e18cb1120bf2116a1bfc8fea0a830e058",
    Path("tests/test_frozen_training.py"): "f1951f17caf419f14c6e5131d470e0f712fa8ffac5c3fb6d48922c05da560d5f",
}

REQUIRED_FILES = (
    Path(".gitattributes"),
    Path(".gitignore"),
    Path("AGENTS.md"),
    Path("CHANGELOG.md"),
    Path("CONTRIBUTING.md"),
    Path("LICENSE"),
    Path("README.md"),
    Path("VERSION"),
    Path("docs/governance/CHECKPOINT-POLICY.md"),
    Path("docs/governance/EXPERIMENT-THREE-EXECUTION-GOAL.md"),
    Path("docs/roadmap/ROADMAP.md"),
    Path("docs/status/STATUS.md"),
    Path("docs/status/VERSION-HISTORY.md"),
    Path("docs/model-card/MODEL-CARD.md"),
    Path("docs/limitations/LIMITATIONS.md"),
    Path("docs/devlog/2026-08-23-empty-bootstrap.md"),
    Path("docs/devlog/2026-08-24-milestone-one-intake.md"),
    Path("docs/devlog/2026-08-24-milestone-two-runtime-gate.md"),
    Path("docs/devlog/2026-08-24-milestone-four-frozen-training.md"),
    Path("docs/devlog/2026-08-25-milestone-five-evaluation.md"),
    Path("records/decisions/DECISION-REGISTER.md"),
    Path("records/evidence/EVIDENCE-LEDGER.md"),
    Path("records/governance/EXPERIMENT-THREE-AUTHORITY-2026-001.md"),
    HISTORICAL_CONTROL_PROFILE,
    MILESTONE_ONE_CONTROL_PROFILE,
    MILESTONE_TWO_CONTROL_PROFILE,
    MILESTONE_THREE_CONTROL_PROFILE,
    MILESTONE_FOUR_CONTROL_PROFILE,
    MILESTONE_FIVE_CONTROL_PROFILE,
    MILESTONE_SIX_CONTROL_PROFILE,
    MILESTONE_SIX_RELEASE_PROFILE,
    CONTROL_PROFILE,
    BOOTSTRAP_MILESTONE,
    PROVENANCE_MILESTONE,
    SYNTHETIC_PREFLIGHT_MILESTONE,
    PROTOCOL_FREEZE_MILESTONE,
    FROZEN_TRAINING_MILESTONE,
    RETROSPECTIVE_EVALUATION_MILESTONE,
    TERMINAL_RELEASE_MILESTONE,
    PREOPENING_AUDIT,
    PREOPENING_VERIFIER,
    EVALUATION_PATH_PREFLIGHT,
    RETROSPECTIVE_EVALUATION_RECORD,
    PUBLIC_EVIDENCE_MANIFEST,
    REVIEWER_EVIDENCE_RECORD,
    REVIEWER_RENDERER,
    RELEASE_SURFACE_MATRIX,
    RELEASE_AUDIT,
    RELEASE_CANDIDATE,
    LIVE_RELEASE_RECORD,
    LIVE_RELEASE_SURFACE_MATRIX,
    LIVE_RELEASE_AUDIT,
    TERMINAL_CLOSEOUT_RECORD,
    Path("scripts/build_release_package.py"),
    Path("scripts/verify_release_package.py"),
    Path("tests/test_release_package.py"),
    Path("records/release/README.md"),
    Path("docs/evidence/REVIEWER-GUIDE.md"),
    Path("docs/evidence/generated/architecture.svg"),
    Path("docs/evidence/generated/training-curves.svg"),
    Path("docs/evidence/generated/comparative-summary.svg"),
    Path("docs/benchmark/BENCHMARK-CARD.md"),
    Path("docs/reproducibility/REPRODUCIBILITY.md"),
    Path("docs/release/RELEASE-NOTES-v1.0.0.md"),
    Path("docs/devlog/2026-08-25-milestone-six-release.md"),
    Path("records/prompt-build-log/2026-08-25-milestone-six-release.md"),
    *EVALUATION_PATH_SOURCES.keys(),
    STATE_RECONCILIATION,
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-002.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-003.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-004.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-005.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-006.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-007.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-008.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-009.json"),
    Path("records/evaluation/README.md"),
    Path("records/prompt-build-log/2026-08-25-milestone-five-evaluation.md"),
    Path("records/training/README.md"),
    TRAIN_VALIDATION_DATA_RECORD,
    FROZEN_TRAINING_RECORD,
    OWNER_RIGHTS_DECISION,
    SOURCE_GATE,
    READINESS_INPUT,
    READINESS_DECISION,
    ADMISSION_MANIFEST,
    INTAKE_RECEIPT,
    RUNTIME_INVENTORY,
    RUNTIME_SOURCE_GATE,
    RUNTIME_REVIEW_ITEM,
    RUNTIME_REVIEW_CONTRACT,
    RUNTIME_BLANK_RESPONSE,
    RUNTIME_ADOPTION_DECISION,
    RUNTIME_ACTIVATION_FAILURE,
    RUNTIME_SUCCESSOR_INVENTORY,
    RUNTIME_SUCCESSOR_SOURCE_GATE,
    RUNTIME_SUCCESSOR_REVIEW_ITEM,
    RUNTIME_SUCCESSOR_REVIEW_CONTRACT,
    RUNTIME_SUCCESSOR_BLANK_RESPONSE,
    RUNTIME_SUCCESSOR_ADOPTION_DECISION,
    RUNTIME_SUCCESSOR_ACTIVATION,
    SYNTHETIC_PREFLIGHT_RECORD,
    Path("protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json"),
    Path("records/protocol/EXPERIMENT-THREE-PROTOCOL-FREEZE-2026-001.json"),
    *SYNTHETIC_SOURCE_IDENTITIES.keys(),
    Path("src/burnlens_experiment_three/protocol.py"),
    Path("src/burnlens_experiment_three/selection.py"),
    Path("src/burnlens_experiment_three/metrics.py"),
    Path("records/prompt-build-log/2026-08-23-bootstrap.md"),
    Path("records/prompt-build-log/2026-08-24-milestone-one-intake.md"),
    Path("records/prompt-build-log/2026-08-24-milestone-two-runtime-gate.md"),
    Path("records/prompt-build-log/2026-08-24-milestone-three-protocol-freeze.md"),
    Path("records/prompt-build-log/2026-08-24-milestone-four-frozen-training.md"),
    Path("docs/devlog/2026-08-24-milestone-three-protocol-freeze.md"),
    Path("scripts/validate_frozen_protocol.py"),
    Path("scripts/run_protocol_dry_run.py"),
    Path("scripts/validate_repository.py"),
    Path("tests/test_repository_controls.py"),
    Path("tests/test_frozen_protocol.py"),
    *FROZEN_TRAINING_SOURCE_IDENTITIES.keys(),
    Path(".github/ISSUE_TEMPLATE/config.yml"),
    Path(".github/ISSUE_TEMPLATE/milestone.yml"),
    Path(".github/pull_request_template.md"),
    Path(".github/workflows/validate.yml"),
)

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "htmlcov",
    "venv",
}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".css",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}

PROHIBITED_ARTIFACT_SUFFIXES = {
    ".ckpt",
    ".h5",
    ".hdf5",
    ".joblib",
    ".jp2",
    ".npy",
    ".npz",
    ".onnx",
    ".parquet",
    ".pickle",
    ".pkl",
    ".pt",
    ".pth",
    ".safetensors",
    ".tif",
    ".tiff",
}

PROHIBITED_ARTIFACT_DIRECTORIES = {
    "artifacts",
    "checkpoints",
    "custody",
    "data",
    "datasets",
    "evaluation",
    "evaluations",
    "inference",
    "models",
    "outputs",
    "predictions",
    "runs",
    "training",
}

EMPTY_OUTPUT_FIELDS = (
    "datasets",
    "training_runs",
    "checkpoints",
    "inference_runs",
    "evaluations",
    "releases",
)

MILESTONE_ONE_ZERO_OUTPUT_FIELDS = (
    "training_runs",
    "checkpoints",
    "inference_runs",
    "evaluations",
    "releases",
)

MILESTONE_ONE_ADMISSION_RECORDS = (
    Path(
        "records/intake/"
        "EXPERIMENT-ONE-BENCHMARK-ADMISSION-MANIFEST-2026-001.json"
    ),
    Path(
        "records/intake/"
        "EXPERIMENT-ONE-BENCHMARK-INTAKE-RECEIPT-2026-001.json"
    ),
)


def _repository_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORY_NAMES for part in relative.parts):
            continue
        yield path


def _relative_name(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _repository_text_sha256(raw: bytes) -> str:
    """Hash canonical LF repository text independent of Windows checkout mode."""

    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def _canonical_roster_sha256(
    entries: list[dict[str, Any]], byte_field: str, hash_field: str
) -> str | None:
    """Hash a recorded identity roster without reading any referenced source bytes."""

    rows: list[tuple[str, str]] = []
    for entry in entries:
        path = entry.get("path")
        byte_count = entry.get(byte_field)
        digest = entry.get(hash_field)
        if (
            not isinstance(path, str)
            or not path
            or type(byte_count) is not int
            or byte_count < 0
            or not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-f]{64}", digest) is None
        ):
            return None
        rows.append((path, f"{path}\t{byte_count}\t{digest}\n"))
    payload = "".join(row for _, row in sorted(rows, key=lambda item: item[0]))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _check_identity_entries(
    entries: Any,
    *,
    label: str,
    expected_count: int,
    expected_bytes: int | None,
    byte_field: str = "observed_bytes",
    hash_field: str = "observed_sha256",
    paired_expected_fields: bool = True,
) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    if not isinstance(entries, list):
        return [f"{label} must be a JSON array"], []
    if len(entries) != expected_count:
        errors.append(f"{label} must contain exactly {expected_count} entries")

    typed_entries: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    aggregate_bytes = 0
    aggregate_valid = True
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{label}[{index}] must be a JSON object")
            aggregate_valid = False
            continue
        typed_entries.append(entry)
        path = entry.get("path")
        if not isinstance(path, str) or not path or "\\" in path:
            errors.append(f"{label}[{index}].path must be a non-empty POSIX path")
        elif path in seen_paths:
            errors.append(f"{label} contains duplicate path: {path}")
        else:
            seen_paths.add(path)

        byte_count = entry.get(byte_field)
        if type(byte_count) is not int or byte_count < 0:
            errors.append(f"{label}[{index}].{byte_field} must be a nonnegative integer")
            aggregate_valid = False
        else:
            aggregate_bytes += byte_count

        digest = entry.get(hash_field)
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            errors.append(f"{label}[{index}].{hash_field} must be lowercase SHA-256")

        if entry.get("integrity_status") != "pass":
            errors.append(f"{label}[{index}].integrity_status must be 'pass'")

        if paired_expected_fields:
            if entry.get("expected_bytes") != byte_count:
                errors.append(
                    f"{label}[{index}] expected_bytes must match {byte_field}"
                )
            if entry.get("expected_sha256") != digest:
                errors.append(
                    f"{label}[{index}] expected_sha256 must match {hash_field}"
                )

    if expected_bytes is not None and (
        not aggregate_valid or aggregate_bytes != expected_bytes
    ):
        errors.append(f"{label} aggregate bytes must equal {expected_bytes}")
    return errors, typed_entries


def check_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        target = root / relative
        if not target.is_file():
            errors.append(f"missing required file: {relative.as_posix()}")
        elif target.stat().st_size == 0:
            errors.append(f"required file is empty: {relative.as_posix()}")
    return errors


def check_json_documents(root: Path) -> list[str]:
    errors: list[str] = []
    for path in _repository_files(root):
        if path.suffix.casefold() != ".json":
            continue
        try:
            _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON: {_relative_name(root, path)}: {exc}")
    return errors


def check_no_cloud_sync_references(root: Path) -> list[str]:
    """Reject operational cloud-sync paths while allowing explicit deny policy."""

    errors: list[str] = []
    marker = "one" + "drive"
    policy_key_cues = (
        "deny",
        "denied",
        "disallow",
        "exclude",
        "forbid",
        "limit",
        "no_go",
        "not_authorize",
        "prohibit",
    )
    prose_policy_cues = (
        "avoid ",
        "denied",
        "do not",
        "excluded",
        "forbidden",
        "must never",
        "must not",
        "never ",
        "no ",
        "no-go",
        "non-",
        "outside ",
        "prohibited",
    )

    def check_json_value(value: Any, path: tuple[str, ...], relative: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                check_json_value(child, path + (str(key).casefold(),), relative)
            return
        if isinstance(value, list):
            for child in value:
                check_json_value(child, path, relative)
            return
        if not isinstance(value, str) or marker not in value.casefold():
            return
        key_context = ".".join(path)
        if not any(cue in key_context for cue in policy_key_cues):
            errors.append(f"forbidden operational cloud-sync reference: {relative}")

    for path in _repository_files(root):
        relative = _relative_name(root, path)
        if marker in relative.casefold():
            errors.append(f"forbidden cloud-sync path: {relative}")
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in {
            "AGENTS.md",
            "LICENSE",
            "VERSION",
        }:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if path.suffix.casefold() == ".json":
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                continue
            check_json_value(parsed, (), relative)
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            folded = line.casefold()
            if marker not in folded:
                continue
            if any(cue in folded for cue in prose_policy_cues):
                continue
            errors.append(
                "forbidden operational cloud-sync reference: "
                f"{relative}:{line_number}"
            )
    return errors


def _active_pre_model_policy(profile: Any) -> str | None:
    """Return the active zero-output policy, if the milestone has one."""

    if not isinstance(profile, dict):
        return "bootstrap"
    active = profile.get("active_milestone_path")
    if not isinstance(active, str):
        return "bootstrap"
    active_name = PurePosixPath(active).name.casefold()
    if "milestone-000" in active_name or "bootstrap" in active_name:
        return "bootstrap"
    if "milestone-001" in active_name or "provenance" in active_name:
        return "milestone_1"
    if "milestone-002" in active_name or "synthetic-preflight" in active_name:
        return "milestone_2"
    if "milestone-003" in active_name or "protocol-freeze" in active_name:
        return "milestone_3"
    return None


def check_no_scientific_artifacts(root: Path) -> list[str]:
    policy = "bootstrap"
    profile_path = root / CONTROL_PROFILE
    if profile_path.is_file():
        try:
            profile = _load_json(profile_path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            profile = None
        policy = _active_pre_model_policy(profile)
        if policy is None:
            return []

    errors: list[str] = []
    policy_label = {
        "bootstrap": "bootstrap",
        "milestone_1": "milestone 1",
        "milestone_2": "milestone 2",
        "milestone_3": "milestone 3",
    }.get(policy, "pre-model")
    for path in _repository_files(root):
        relative = path.relative_to(root)
        suffix = path.suffix.casefold()
        if suffix in PROHIBITED_ARTIFACT_SUFFIXES:
            errors.append(
                f"prohibited {policy_label} artifact type: {relative.as_posix()}"
            )
            continue
        directory_parts = {part.casefold() for part in relative.parts[:-1]}
        forbidden_parts = directory_parts & PROHIBITED_ARTIFACT_DIRECTORIES
        if forbidden_parts:
            errors.append(
                f"prohibited {policy_label} artifact location: {relative.as_posix()}"
            )
    return errors


def _checked_relative_path(value: Any, field: str) -> tuple[Path | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, f"{field} must be a non-empty repository-relative path"
    if "\\" in value:
        return None, f"{field} must use forward slashes"
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or re.match(r"^[A-Za-z]:", value):
        return None, f"{field} must stay within the repository"
    if "://" in value:
        return None, f"{field} must not be a URL"
    return Path(*pure.parts), None


def _path_stays_under(root: Path, target: Path) -> bool:
    try:
        return os.path.commonpath((str(root.resolve()), str(target.resolve()))) == str(
            root.resolve()
        )
    except ValueError:
        return False


def check_control_references(root: Path) -> list[str]:
    errors: list[str] = []
    profile_path = root / CONTROL_PROFILE
    if not profile_path.is_file():
        return errors
    try:
        profile = _load_json(profile_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors
    if not isinstance(profile, dict):
        return [f"control profile must be a JSON object: {CONTROL_PROFILE.as_posix()}"]

    active_relative, error = _checked_relative_path(
        profile.get("active_milestone_path"), "active_milestone_path"
    )
    if error:
        return [error]
    assert active_relative is not None
    active_path = root / active_relative
    if not _path_stays_under(root, active_path):
        return ["active_milestone_path resolves outside the repository"]
    if not active_path.is_file():
        return [f"active milestone does not exist: {active_relative.as_posix()}"]

    try:
        milestone = _load_json(active_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors
    if not isinstance(milestone, dict):
        return [f"active milestone must be a JSON object: {active_relative.as_posix()}"]

    profile_relative, error = _checked_relative_path(
        milestone.get("control_profile_path"), "control_profile_path"
    )
    if error:
        return [error]
    assert profile_relative is not None
    if profile_relative.as_posix() != CONTROL_PROFILE.as_posix():
        errors.append(
            "active milestone control_profile_path must point to "
            f"{CONTROL_PROFILE.as_posix()}"
        )
    referenced_profile = root / profile_relative
    if not _path_stays_under(root, referenced_profile):
        errors.append("control_profile_path resolves outside the repository")
    elif not referenced_profile.is_file():
        errors.append(f"control profile does not exist: {profile_relative.as_posix()}")
    return errors


def check_truthful_bootstrap_state(root: Path) -> list[str]:
    """Require explicit zero scientific outputs in active pre-model milestones."""

    errors: list[str] = []
    profile_path = root / CONTROL_PROFILE
    if not profile_path.is_file():
        return errors
    try:
        profile = _load_json(profile_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors
    if not isinstance(profile, dict):
        return errors

    policy = _active_pre_model_policy(profile)
    if policy is None:
        return errors
    policy_label = {
        "bootstrap": "bootstrap",
        "milestone_1": "milestone 1",
        "milestone_2": "milestone 2",
        "milestone_3": "milestone 3",
    }.get(policy, "pre-model")

    active_relative, error = _checked_relative_path(
        profile.get("active_milestone_path"), "active_milestone_path"
    )
    if error or active_relative is None:
        return errors

    state = profile.get("scientific_state")
    if not isinstance(state, str) or state.casefold() != "not_started":
        errors.append(f"{policy_label} scientific_state must be 'not_started'")

    profile_outputs = profile.get("scientific_outputs")
    if policy in {"milestone_1", "milestone_2", "milestone_3"} and not isinstance(profile_outputs, dict):
        errors.append(f"{policy_label} profile scientific_outputs must be a JSON object")

    milestone_path = root / active_relative
    if not milestone_path.is_file():
        return errors
    try:
        milestone = _load_json(milestone_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors
    if not isinstance(milestone, dict):
        return errors
    outputs = milestone.get("scientific_outputs")
    if not isinstance(outputs, dict):
        return errors + [
            f"{policy_label} milestone scientific_outputs must be a JSON object"
        ]
    zero_fields = (
        EMPTY_OUTPUT_FIELDS
        if policy == "bootstrap"
        else MILESTONE_ONE_ZERO_OUTPUT_FIELDS
    )
    for field in zero_fields:
        value = outputs.get(field)
        if type(value) is not int or value != 0:
            errors.append(
                f"{policy_label} milestone "
                f"scientific_outputs.{field} must be integer 0"
            )

    if policy in {"milestone_1", "milestone_2", "milestone_3"} and isinstance(profile_outputs, dict):
        for field in MILESTONE_ONE_ZERO_OUTPUT_FIELDS:
            value = profile_outputs.get(field)
            if type(value) is not int or value != 0:
                errors.append(
                    f"{policy_label} profile "
                    f"scientific_outputs.{field} must be integer 0"
                )

        profile_datasets = profile_outputs.get("datasets")
        milestone_datasets = outputs.get("datasets")
        for location, value in (
            ("profile", profile_datasets),
            ("milestone", milestone_datasets),
        ):
            if type(value) is not int or value not in (0, 1):
                errors.append(
                    f"{policy_label} {location} scientific_outputs.datasets "
                    + ("must be integer 1" if policy in {"milestone_2", "milestone_3"} else "must be integer 0 or 1")
                )
        if (
            type(profile_datasets) is int
            and type(milestone_datasets) is int
            and profile_datasets != milestone_datasets
        ):
            errors.append(
                f"{policy_label} profile and milestone "
                "scientific_outputs.datasets must match"
            )

        if policy in {"milestone_2", "milestone_3"} and (
            profile_datasets != 1 or milestone_datasets != 1
        ):
            errors.append(f"{policy_label} requires exactly one admitted dataset")

    if policy == "milestone_1" and isinstance(profile_outputs, dict):
        units = milestone.get("units")
        intake_unit = None
        if isinstance(units, list):
            intake_unit = next(
                (
                    unit
                    for unit in units
                    if isinstance(unit, dict)
                    and unit.get("id")
                    == "M1-U005-CONTROLLED-BENCHMARK-INTAKE"
                ),
                None,
            )

        admitted_dataset = (
            type(profile_datasets) is int
            and type(milestone_datasets) is int
            and profile_datasets == milestone_datasets == 1
        )
        if admitted_dataset:
            if not isinstance(intake_unit, dict):
                errors.append(
                    "milestone 1 dataset admission requires the controlled-intake unit"
                )
            elif (
                intake_unit.get("status") != "complete"
                or intake_unit.get("disposition") != "pass"
            ):
                errors.append(
                    "milestone 1 dataset admission requires controlled intake "
                    "status complete with disposition pass"
                )

        if (
            admitted_dataset
            or isinstance(intake_unit, dict)
            and intake_unit.get("status") == "complete"
        ):
            for relative in MILESTONE_ONE_ADMISSION_RECORDS:
                record_path = root / relative
                if not record_path.is_file():
                    errors.append(
                        "milestone 1 dataset admission record is missing: "
                        f"{relative.as_posix()}"
                    )
                    continue
                try:
                    record = _load_json(record_path)
                except (OSError, UnicodeError, json.JSONDecodeError):
                    errors.append(
                        "milestone 1 dataset admission record is invalid JSON: "
                        f"{relative.as_posix()}"
                    )
                    continue
                if not isinstance(record, dict) or not record:
                    errors.append(
                        "milestone 1 dataset admission record must be a non-empty "
                        f"JSON object: {relative.as_posix()}"
                    )
    return errors


def check_milestone_one_identity_inventory(root: Path) -> list[str]:
    """Bind a completed M1-U002 claim to its repository-owned identity record."""

    profile_path = root / CONTROL_PROFILE
    if not profile_path.is_file():
        return []
    try:
        profile = _load_json(profile_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return []
    if not isinstance(profile, dict) or _active_pre_model_policy(profile) != "milestone_1":
        return []

    active_relative, path_error = _checked_relative_path(
        profile.get("active_milestone_path"), "active_milestone_path"
    )
    if path_error or active_relative is None:
        return []
    milestone_path = root / active_relative
    if not milestone_path.is_file():
        return []
    try:
        milestone = _load_json(milestone_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return []
    if not isinstance(milestone, dict):
        return []

    units = milestone.get("units")
    if not isinstance(units, list):
        return []
    identity_units = [
        unit
        for unit in units
        if isinstance(unit, dict)
        and unit.get("id") == "M1-U002-READ-ONLY-IDENTITY-INVENTORY"
    ]
    completed_units = [unit for unit in identity_units if unit.get("status") == "complete"]
    if not completed_units:
        return []

    errors: list[str] = []
    if len(identity_units) != 1:
        errors.append("milestone 1 must contain exactly one M1-U002 identity unit")
    identity_unit = completed_units[0]
    expected_unit_gates = {
        "source_repository_read_only": "pass",
        "exact_git_and_path_identity": "pass",
        "sha256_every_candidate": "pass",
        "role_and_exposure_classification": "pass",
        "missing_rejected_ambiguous_retained": "pass",
    }
    if identity_unit.get("disposition") != "pass":
        errors.append("completed M1-U002 disposition must be 'pass'")
    unit_outputs = identity_unit.get("outputs")
    if (
        not isinstance(unit_outputs, list)
        or PROVENANCE_IDENTITY_INVENTORY.as_posix() not in unit_outputs
    ):
        errors.append("completed M1-U002 must name the identity inventory output")
    unit_gates = identity_unit.get("gates")
    if not isinstance(unit_gates, dict):
        errors.append("completed M1-U002 gates must be a JSON object")
    else:
        for field, expected in expected_unit_gates.items():
            if unit_gates.get(field) != expected:
                errors.append(f"completed M1-U002 gates.{field} must be '{expected}'")
    exit_delta = identity_unit.get("exit_condition_delta")
    if not isinstance(exit_delta, dict):
        errors.append("completed M1-U002 exit_condition_delta must be a JSON object")
    else:
        for field in ("expected", "observed"):
            if exit_delta.get(field) != ["EXIT-M1-IDENTITY"]:
                errors.append(
                    f"completed M1-U002 exit_condition_delta.{field} "
                    "must contain only EXIT-M1-IDENTITY"
                )
        if exit_delta.get("decision_value") != "advances_exit":
            errors.append(
                "completed M1-U002 exit_condition_delta.decision_value must be "
                "'advances_exit'"
            )

    exit_conditions = milestone.get("exit_conditions")
    identity_exits = (
        [
            condition
            for condition in exit_conditions
            if isinstance(condition, dict)
            and condition.get("id") == "EXIT-M1-IDENTITY"
        ]
        if isinstance(exit_conditions, list)
        else []
    )
    if len(identity_exits) != 1:
        errors.append("milestone 1 must contain exactly one EXIT-M1-IDENTITY condition")
    else:
        identity_exit = identity_exits[0]
        if identity_exit.get("status") != "pass":
            errors.append("EXIT-M1-IDENTITY status must be 'pass' after U002 completion")
        exit_evidence = identity_exit.get("evidence")
        if (
            not isinstance(exit_evidence, list)
            or PROVENANCE_IDENTITY_INVENTORY.as_posix() not in exit_evidence
        ):
            errors.append("EXIT-M1-IDENTITY must cite the identity inventory")

    inventory_path = root / PROVENANCE_IDENTITY_INVENTORY
    if not inventory_path.is_file():
        return errors + [
            "completed M1-U002 identity inventory is missing: "
            f"{PROVENANCE_IDENTITY_INVENTORY.as_posix()}"
        ]
    if inventory_path.stat().st_size == 0:
        return errors + ["completed M1-U002 identity inventory must be non-empty"]
    try:
        inventory = _load_json(inventory_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors + ["completed M1-U002 identity inventory must be valid JSON"]
    if not isinstance(inventory, dict) or not inventory:
        return errors + [
            "completed M1-U002 identity inventory must be a non-empty JSON object"
        ]

    if inventory.get("inventory_id") != EXPECTED_PROVENANCE_INVENTORY_ID:
        errors.append(
            "M1-U002 inventory_id must equal "
            f"{EXPECTED_PROVENANCE_INVENTORY_ID}"
        )
    if inventory.get("milestone_ref") != active_relative.as_posix():
        errors.append("M1-U002 inventory milestone_ref must name the active milestone")
    if inventory.get("inspection_mode") != "read_only_metadata_only_no_copy_no_execution":
        errors.append("M1-U002 inventory inspection_mode is inconsistent")

    source = inventory.get("source_repository")
    if not isinstance(source, dict):
        errors.append("M1-U002 source_repository must be a JSON object")
    else:
        exact_source_fields = {
            "path": r"C:\Projects\Active\burnlens-deschutes",
            "remote": "https://github.com/drwbkr1/burnlens-deschutes.git",
            "branch": "main",
            "head": EXPECTED_EXPERIMENT_ONE_HEAD,
            "origin_main": EXPECTED_EXPERIMENT_ONE_HEAD,
            "tree": EXPECTED_EXPERIMENT_ONE_TREE,
        }
        for field, expected in exact_source_fields.items():
            if source.get(field) != expected:
                errors.append(
                    f"M1-U002 source_repository.{field} must equal {expected}"
                )
        if source.get("worktree_clean") is not True:
            errors.append("M1-U002 source_repository.worktree_clean must be true")
        if source.get("source_mutated") is not False:
            errors.append("M1-U002 source_repository.source_mutated must be false")

    identity_summary = inventory.get("identity_summary")
    if not isinstance(identity_summary, dict):
        errors.append("M1-U002 identity_summary must be a JSON object")
        identity_summary = {}
    summary_fields = {
        "repository_identity": "pass",
        "dataset_array_count": 48,
        "dataset_array_bytes": 1333248,
        "dataset_array_mismatches": 0,
        "supplemental_transitive_record_count": 5,
        "unet_prediction_array_count": 8,
        "unet_prediction_array_bytes": 82944,
        "bytes_copied_to_experiment_three": 0,
        "source_code_files_executed": 0,
        "npy_or_pt_files_loaded_or_deserialized": 0,
    }
    for field, expected in summary_fields.items():
        if identity_summary.get(field) != expected:
            errors.append(f"M1-U002 identity_summary.{field} must equal {expected}")

    dataset = inventory.get("dataset")
    if not isinstance(dataset, dict):
        errors.append("M1-U002 dataset must be a JSON object")
        dataset = {}
    array_errors, dataset_arrays = _check_identity_entries(
        dataset.get("arrays"),
        label="M1-U002 dataset arrays",
        expected_count=48,
        expected_bytes=1333248,
    )
    errors.extend(array_errors)
    dataset_roster = dataset.get("array_roster")
    if not isinstance(dataset_roster, dict):
        errors.append("M1-U002 dataset array_roster must be a JSON object")
        dataset_roster = {}
    expected_dataset_roster = {
        "sha256": EXPECTED_DATASET_ROSTER_SHA256,
        "file_count": 48,
        "aggregate_bytes": 1333248,
        "all_match": True,
    }
    for field, expected in expected_dataset_roster.items():
        actual = dataset_roster.get(field)
        if (type(expected) is bool and actual is not expected) or (
            type(expected) is not bool and actual != expected
        ):
            errors.append(f"M1-U002 dataset array_roster.{field} must equal {expected}")
    calculated_dataset_sha = _canonical_roster_sha256(
        dataset_arrays, "observed_bytes", "observed_sha256"
    )
    if calculated_dataset_sha != EXPECTED_DATASET_ROSTER_SHA256:
        errors.append(
            "M1-U002 dataset array roster SHA-256 does not match its canonical "
            "terminal-LF identity"
        )

    source_terms = inventory.get("source_and_terms_evidence")
    if not isinstance(source_terms, dict):
        errors.append("M1-U002 source_and_terms_evidence must be a JSON object")
        source_terms = {}
    direct_bindings = source_terms.get("direct_bindings")
    direct_summary = source_terms.get("direct_binding_summary")
    expected_direct_counts = {
        "proposals": 5,
        "owner_intakes": 5,
        "source_records": 13,
        "terms_records": 14,
    }
    checked_direct: dict[str, list[dict[str, Any]]] = {}
    if not isinstance(direct_bindings, dict):
        errors.append("M1-U002 direct_bindings must be a JSON object")
        direct_bindings = {}
    if not isinstance(direct_summary, dict):
        errors.append("M1-U002 direct_binding_summary must be a JSON object")
        direct_summary = {}
    for role, expected_count in expected_direct_counts.items():
        binding_errors, entries = _check_identity_entries(
            direct_bindings.get(role),
            label=f"M1-U002 direct bindings {role}",
            expected_count=expected_count,
            expected_bytes=None,
        )
        errors.extend(binding_errors)
        checked_direct[role] = entries
        role_summary = direct_summary.get(role)
        if not isinstance(role_summary, dict):
            errors.append(f"M1-U002 direct_binding_summary.{role} must be an object")
            continue
        observed_total = sum(
            entry.get("observed_bytes", 0)
            for entry in entries
            if type(entry.get("observed_bytes")) is int
        )
        if role_summary.get("count") != expected_count:
            errors.append(
                f"M1-U002 direct_binding_summary.{role}.count must equal "
                f"{expected_count}"
            )
        if role_summary.get("bytes") != observed_total:
            errors.append(
                f"M1-U002 direct_binding_summary.{role}.bytes must match its entries"
            )
        if role_summary.get("all_match") is not True:
            errors.append(
                f"M1-U002 direct_binding_summary.{role}.all_match must be true"
            )

    summary_counts = identity_summary.get("direct_binding_counts")
    summary_mismatches = identity_summary.get("direct_binding_mismatches")
    if not isinstance(summary_counts, dict):
        errors.append("M1-U002 identity_summary.direct_binding_counts must be an object")
    else:
        for role, expected_count in expected_direct_counts.items():
            if summary_counts.get(role) != expected_count:
                errors.append(
                    f"M1-U002 identity_summary.direct_binding_counts.{role} "
                    f"must equal {expected_count}"
                )
    if not isinstance(summary_mismatches, dict):
        errors.append(
            "M1-U002 identity_summary.direct_binding_mismatches must be an object"
        )
    else:
        for role in expected_direct_counts:
            if summary_mismatches.get(role) != 0:
                errors.append(
                    f"M1-U002 identity_summary.direct_binding_mismatches.{role} "
                    "must equal 0"
                )

    supplemental_errors, supplemental_entries = _check_identity_entries(
        source_terms.get("supplemental_transitive_chain"),
        label="M1-U002 supplemental transitive records",
        expected_count=5,
        expected_bytes=None,
        byte_field="bytes",
        hash_field="sha256",
        paired_expected_fields=False,
    )
    errors.extend(supplemental_errors)
    source_roster = source_terms.get("source_terms_roster")
    if not isinstance(source_roster, dict):
        errors.append("M1-U002 source_terms_roster must be a JSON object")
        source_roster = {}
    expected_source_roster = {
        "file_count": 32,
        "aggregate_bytes": 164639,
        "sha256": EXPECTED_SOURCE_TERMS_ROSTER_SHA256,
        "all_match": True,
    }
    for field, expected in expected_source_roster.items():
        actual = source_roster.get(field)
        if (type(expected) is bool and actual is not expected) or (
            type(expected) is not bool and actual != expected
        ):
            errors.append(f"M1-U002 source_terms_roster.{field} must equal {expected}")
    normalized_source_entries = [
        {
            "path": entry.get("path"),
            "bytes": entry.get("observed_bytes"),
            "sha256": entry.get("observed_sha256"),
        }
        for role in ("source_records", "terms_records")
        for entry in checked_direct.get(role, [])
    ] + supplemental_entries
    calculated_source_sha = _canonical_roster_sha256(
        normalized_source_entries, "bytes", "sha256"
    )
    if calculated_source_sha != EXPECTED_SOURCE_TERMS_ROSTER_SHA256:
        errors.append(
            "M1-U002 source/terms roster SHA-256 does not match its canonical "
            "terminal-LF identity"
        )

    comparison = inventory.get("comparison_artifacts")
    canonical_unet = (
        comparison.get("canonical_unet") if isinstance(comparison, dict) else None
    )
    if not isinstance(canonical_unet, dict):
        errors.append("M1-U002 canonical_unet must be a JSON object")
        canonical_unet = {}
    prediction_errors, predictions = _check_identity_entries(
        canonical_unet.get("predictions"),
        label="M1-U002 U-Net predictions",
        expected_count=8,
        expected_bytes=82944,
    )
    errors.extend(prediction_errors)
    for index, prediction in enumerate(predictions):
        path = prediction.get("path")
        if isinstance(path, str) and not path.startswith("predictions/"):
            errors.append(
                f"M1-U002 U-Net predictions[{index}].path must be "
                "evaluation-root-relative under predictions/"
            )
    prediction_roster = canonical_unet.get("prediction_roster")
    if not isinstance(prediction_roster, dict):
        errors.append("M1-U002 U-Net prediction_roster must be a JSON object")
        prediction_roster = {}
    expected_prediction_roster = {
        "sha256": EXPECTED_UNET_PREDICTION_ROSTER_SHA256,
        "file_count": 8,
        "aggregate_bytes": 82944,
        "all_match": True,
    }
    for field, expected in expected_prediction_roster.items():
        actual = prediction_roster.get(field)
        if (type(expected) is bool and actual is not expected) or (
            type(expected) is not bool and actual != expected
        ):
            errors.append(
                f"M1-U002 U-Net prediction_roster.{field} must equal {expected}"
            )
    calculated_prediction_sha = _canonical_roster_sha256(
        predictions, "observed_bytes", "observed_sha256"
    )
    if calculated_prediction_sha != EXPECTED_UNET_PREDICTION_ROSTER_SHA256:
        errors.append(
            "M1-U002 U-Net prediction roster SHA-256 does not match its canonical "
            "evaluation-root-relative terminal-LF identity"
        )

    lanes = inventory.get("lane_dispositions")
    if not isinstance(lanes, dict):
        errors.append("M1-U002 lane_dispositions must be a JSON object")
        lanes = {}
    expected_lanes: dict[str, Any] = {
        "metadata_identity": "PASS",
        "controlled_local_copy": "DEFER",
        "downstream_scientific_use": "DEFER",
        "repository_redistribution": "BLOCK",
        "raw_provider_redistribution": "BLOCK",
        "bytes_copied": 0,
        "custody_directory_created": False,
    }
    for field, expected in expected_lanes.items():
        actual = lanes.get(field)
        if (type(expected) is bool and actual is not expected) or (
            type(expected) is int
            and (type(actual) is not int or actual != expected)
        ) or (type(expected) not in (bool, int) and actual != expected):
            errors.append(f"M1-U002 lane_dispositions.{field} must equal {expected}")

    inventory_gates = inventory.get("gates")
    if not isinstance(inventory_gates, dict):
        errors.append("M1-U002 inventory gates must be a JSON object")
    else:
        for field, expected in expected_unit_gates.items():
            if inventory_gates.get(field) != expected:
                errors.append(f"M1-U002 inventory gates.{field} must be '{expected}'")
        if (
            inventory_gates.get("source_rights")
            != "pending_human_gate_not_an_identity_failure"
        ):
            errors.append("M1-U002 inventory gates.source_rights is inconsistent")
        if inventory_gates.get("benchmark_intake") != "not_authorized":
            errors.append("M1-U002 inventory gates.benchmark_intake is inconsistent")
    if inventory.get("disposition") != "pass_identity_metadata_only":
        errors.append("M1-U002 inventory disposition is inconsistent")

    outputs_created = inventory.get("scientific_outputs_created")
    if not isinstance(outputs_created, dict):
        errors.append("M1-U002 scientific_outputs_created must be a JSON object")
    else:
        if set(outputs_created) != set(EMPTY_OUTPUT_FIELDS):
            errors.append(
                "M1-U002 scientific_outputs_created must contain exactly the "
                "declared scientific output fields"
            )
        for field in EMPTY_OUTPUT_FIELDS:
            value = outputs_created.get(field)
            if type(value) is not int or value != 0:
                errors.append(
                    f"M1-U002 scientific_outputs_created.{field} must be integer 0"
                )
    return errors


def check_owner_rights_review_preparation(root: Path) -> list[str]:
    """Keep the prepared bundle exact and bind either pending or resolved state."""

    milestone_path = root / PROVENANCE_MILESTONE
    if not milestone_path.is_file():
        return []
    try:
        milestone = _load_json(milestone_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return []
    if not isinstance(milestone, dict):
        return []
    human_gates = milestone.get("human_gates")
    if not isinstance(human_gates, list):
        return []
    gates = [
        gate
        for gate in human_gates
        if isinstance(gate, dict)
        and gate.get("id") == "M1-GATE-OWNER-ARTIFACT-RIGHTS"
    ]
    if len(gates) != 1:
        return []
    preparation = gates[0].get("review_preparation")
    if preparation is None:
        return []

    errors: list[str] = []
    if not isinstance(preparation, dict):
        return ["owner-rights review_preparation must be a JSON object"]
    resolved = gates[0].get("status") == "passed"
    expected_preparation: dict[str, Any] = {
        "review_id": EXPECTED_OWNER_REVIEW_ID,
        "review_item_path": OWNER_RIGHTS_REVIEW_ITEM.as_posix(),
        "review_item_sha256": EXPECTED_OWNER_REVIEW_ITEM_SHA256,
        "review_contract_path": OWNER_RIGHTS_REVIEW_CONTRACT.as_posix(),
        "review_contract_sha256": EXPECTED_OWNER_REVIEW_CONTRACT_SHA256,
        "blank_response_path": OWNER_RIGHTS_BLANK_RESPONSE.as_posix(),
        "blank_response_sha256": EXPECTED_OWNER_RIGHTS_BLANK_SHA256,
        "human_decisions_created": 1 if resolved else 0,
        "handoff_state": (
            "completed_locked_and_reconciled"
            if resolved
            else "ready_to_handoff_and_wait"
        ),
    }
    for field, expected in expected_preparation.items():
        actual = preparation.get(field)
        if type(expected) is int:
            if type(actual) is not int or actual != expected:
                errors.append(
                    f"owner-rights review_preparation.{field} must equal {expected}"
                )
        elif actual != expected:
            errors.append(
                f"owner-rights review_preparation.{field} must equal {expected}"
            )

    file_expectations = (
        (OWNER_RIGHTS_REVIEW_ITEM, EXPECTED_OWNER_REVIEW_ITEM_SHA256),
        (OWNER_RIGHTS_REVIEW_CONTRACT, EXPECTED_OWNER_REVIEW_CONTRACT_SHA256),
        (OWNER_RIGHTS_BLANK_RESPONSE, EXPECTED_OWNER_RIGHTS_BLANK_SHA256),
    )
    documents: dict[Path, dict[str, Any]] = {}
    for relative, expected_sha256 in file_expectations:
        path = root / relative
        if not path.is_file():
            errors.append(f"prepared owner-rights review file is missing: {relative.as_posix()}")
            continue
        raw = path.read_bytes()
        if _repository_text_sha256(raw) != expected_sha256:
            errors.append(
                f"prepared owner-rights review file hash changed: {relative.as_posix()}"
            )
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            errors.append(
                f"prepared owner-rights review file must be UTF-8 JSON: {relative.as_posix()}"
            )
            continue
        if not isinstance(value, dict):
            errors.append(
                f"prepared owner-rights review file must be a JSON object: {relative.as_posix()}"
            )
            continue
        documents[relative] = value

    item = documents.get(OWNER_RIGHTS_REVIEW_ITEM)
    if item is not None:
        if item.get("template") is not False:
            errors.append("owner-rights review item template must be false")
        if item.get("review_id") != EXPECTED_OWNER_REVIEW_ID:
            errors.append("owner-rights review item review_id changed")
        if item.get("item_id") != EXPECTED_OWNER_REVIEW_ITEM_ID:
            errors.append("owner-rights review item item_id changed")
        allowed_decisions = item.get("allowed_decisions")
        if (
            not isinstance(allowed_decisions, dict)
            or set(allowed_decisions) != {"yes", "no"}
            or any(
                not isinstance(value, str) or not value
                for value in allowed_decisions.values()
            )
        ):
            errors.append("owner-rights review item must define only nonempty yes/no decisions")

    contract = documents.get(OWNER_RIGHTS_REVIEW_CONTRACT)
    if contract is not None:
        if contract.get("template") is not False:
            errors.append("owner-rights review contract template must be false")
        if contract.get("review_id") != EXPECTED_OWNER_REVIEW_ID:
            errors.append("owner-rights review contract review_id changed")
        if contract.get("allowed_decisions") != ["yes", "no"]:
            errors.append("owner-rights review contract decisions must be yes/no")
        if contract.get("required_attestation") is not True:
            errors.append("owner-rights review contract must require attestation")
        expected_items = [
            {
                "item_id": EXPECTED_OWNER_REVIEW_ITEM_ID,
                "evidence_sha256": EXPECTED_OWNER_REVIEW_ITEM_SHA256,
            }
        ]
        if contract.get("items") != expected_items:
            errors.append("owner-rights review contract item binding changed")

    blank = documents.get(OWNER_RIGHTS_BLANK_RESPONSE)
    if blank is not None:
        expected_responses = [
            {
                "item_id": EXPECTED_OWNER_REVIEW_ITEM_ID,
                "evidence_sha256": EXPECTED_OWNER_REVIEW_ITEM_SHA256,
                "decision": None,
                "notes": "",
            }
        ]
        if blank.get("review_id") != EXPECTED_OWNER_REVIEW_ID:
            errors.append("owner-rights blank response review_id changed")
        if blank.get("completed") is not False:
            errors.append("owner-rights blank response must remain incomplete")
        if blank.get("review_started_at_utc") is not None or blank.get(
            "review_completed_at_utc"
        ) is not None:
            errors.append("owner-rights blank response timestamps must remain null")
        if blank.get("reviewer") != {"attestation": False}:
            errors.append("owner-rights blank response attestation must remain false")
        if blank.get("responses") != expected_responses:
            errors.append("owner-rights blank response must contain zero decisions")

    if resolved:
        if preparation.get("decision_record") != OWNER_RIGHTS_DECISION.as_posix():
            errors.append("resolved owner-rights review must bind the public decision record")
        decision_path = root / OWNER_RIGHTS_DECISION
        if not decision_path.is_file():
            errors.append("resolved owner-rights decision record is missing")
        else:
            raw = decision_path.read_bytes()
            if _repository_text_sha256(raw) != EXPECTED_OWNER_RIGHTS_DECISION_SHA256:
                errors.append("resolved owner-rights decision record hash changed")
            try:
                decision = json.loads(raw.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                decision = None
                errors.append("resolved owner-rights decision must be UTF-8 JSON")
            if isinstance(decision, dict):
                aggregate = decision.get("aggregate")
                locked = decision.get("locked_review_evidence")
                if decision.get("review_id") != EXPECTED_OWNER_REVIEW_ID:
                    errors.append("resolved owner-rights decision review_id changed")
                if decision.get("decision") != "yes":
                    errors.append("resolved owner-rights decision must equal yes")
                if not isinstance(aggregate, dict) or any(
                    aggregate.get(key) != value
                    for key, value in {
                        "expected_decisions": 1,
                        "received_decisions": 1,
                        "yes": 1,
                        "no": 0,
                        "ambiguous": 0,
                        "missing": 0,
                        "attestation_satisfied": True,
                        "exact_bundle_match": True,
                        "human_decisions_fabricated": False,
                    }.items()
                ):
                    errors.append("resolved owner-rights aggregate is inconsistent")
                if (
                    not isinstance(locked, dict)
                    or locked.get("raw_response_or_notes_committed") is not False
                ):
                    errors.append("raw owner-rights response or notes must not be committed")
                outcome = gates[0].get("review_outcome")
                if not isinstance(outcome, dict) or any(
                    outcome.get(key) != value
                    for key, value in {
                        "decision": "yes",
                        "received_decisions": 1,
                        "ambiguous": 0,
                        "raw_response_committed": False,
                    }.items()
                ):
                    errors.append("resolved owner-rights milestone outcome is inconsistent")
                elif isinstance(locked, dict) and (
                    outcome.get("response_sha256") != locked.get("response_sha256")
                    or outcome.get("reconciliation_sha256")
                    != locked.get("reconciliation_sha256")
                ):
                    errors.append("resolved owner-rights private evidence hashes disagree")

        source_path = root / SOURCE_GATE
        if not source_path.is_file():
            errors.append("resolved owner-rights review requires the source-gate record")
        else:
            try:
                source_gate = _load_json(source_path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                source_gate = None
            if (
                not isinstance(source_gate, dict)
                or not isinstance(source_gate.get("decision"), dict)
                or source_gate["decision"].get("status") != "ready"
            ):
                errors.append("resolved owner-rights downstream source gate must be ready")
    return errors


def check_milestone_one_admission_chain(root: Path) -> list[str]:
    """Bind the admitted dataset count to immutable gate, audit, and intake receipts."""

    records = {
        OWNER_RIGHTS_DECISION: EXPECTED_OWNER_RIGHTS_DECISION_SHA256,
        SOURCE_GATE: EXPECTED_SOURCE_GATE_SHA256,
        READINESS_INPUT: EXPECTED_READINESS_INPUT_SHA256,
        READINESS_DECISION: EXPECTED_READINESS_DECISION_SHA256,
        ADMISSION_MANIFEST: EXPECTED_ADMISSION_MANIFEST_SHA256,
        INTAKE_RECEIPT: EXPECTED_INTAKE_RECEIPT_SHA256,
    }
    loaded: dict[Path, dict[str, Any]] = {}
    errors: list[str] = []
    if not (root / INTAKE_RECEIPT).is_file():
        return errors
    for relative, expected_sha in records.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"admission-chain record is missing: {relative.as_posix()}")
            continue
        raw = path.read_bytes()
        if _repository_text_sha256(raw) != expected_sha:
            errors.append(f"admission-chain record hash changed: {relative.as_posix()}")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            errors.append(f"admission-chain record is invalid JSON: {relative.as_posix()}")
            continue
        if isinstance(value, dict):
            loaded[relative] = value

    source_gate = loaded.get(SOURCE_GATE, {})
    readiness = loaded.get(READINESS_DECISION, {})
    readiness_input = loaded.get(READINESS_INPUT, {})
    manifest = loaded.get(ADMISSION_MANIFEST, {})
    receipt = loaded.get(INTAKE_RECEIPT, {})
    if source_gate.get("decision", {}).get("status") != "ready":
        errors.append("admission chain requires source-gate ready")
    if readiness.get("decision") != "pass":
        errors.append("admission chain requires readiness pass")
    if readiness.get("training_authorized") is not False:
        errors.append("readiness decision must not authorize training")
    input_raw = root / READINESS_INPUT
    if input_raw.is_file() and readiness.get(
        "audit_input_sha256"
    ) != _repository_text_sha256(input_raw.read_bytes()):
        errors.append("readiness decision input hash does not match")

    manifest_assets = manifest.get("assets")
    receipt_assets = receipt.get("assets")
    if not isinstance(manifest_assets, list) or len(manifest_assets) != EXPECTED_INTAKE_ASSET_COUNT:
        errors.append("admission manifest must enumerate exactly 131 assets")
    if not isinstance(receipt_assets, list) or len(receipt_assets) != EXPECTED_INTAKE_ASSET_COUNT:
        errors.append("intake receipt must enumerate exactly 131 assets")
    if isinstance(manifest_assets, list) and isinstance(receipt_assets, list):
        manifest_identity = [
            (a.get("asset_id"), a.get("destination_relative_path"), a.get("expected"))
            for a in manifest_assets if isinstance(a, dict)
        ]
        receipt_identity = [
            (a.get("asset_id"), a.get("destination_relative_path"), a.get("expected"))
            for a in receipt_assets if isinstance(a, dict)
        ]
        if manifest_identity != receipt_identity:
            errors.append("admission manifest and intake receipt asset identities disagree")
        if any(a.get("state") != "promoted" for a in receipt_assets if isinstance(a, dict)):
            errors.append("every intake receipt asset must be promoted")
        promoted_bytes = sum(
            a.get("observed", {}).get("promoted_size_bytes", 0)
            for a in receipt_assets if isinstance(a, dict)
        )
        if promoted_bytes != EXPECTED_INTAKE_BYTES:
            errors.append("intake receipt promoted-byte sum must equal 3369748")
    completion = receipt.get("extensions", {}).get("completion", {})
    for field, expected in {
        "promoted_assets": EXPECTED_INTAKE_ASSET_COUNT,
        "promoted_bytes": EXPECTED_INTAKE_BYTES,
        "destination_roster_sha256": EXPECTED_INTAKE_ROSTER_SHA256,
        "staging_reverified": True,
        "destination_reverified": True,
        "source_identity_reverified_before_transfer": True,
        "source_repository_unchanged": True,
        "identity_mismatches": 0,
        "destination_collisions": 0,
        "overwrite_events": 0,
    }.items():
        if completion.get(field) != expected:
            errors.append(f"intake receipt completion.{field} is inconsistent")
    if receipt.get("extensions", {}).get("training_authority_created") is not False:
        errors.append("intake receipt must not create training authority")
    return errors


def check_runtime_adoption_review_preparation(root: Path) -> list[str]:
    """Bind the exact M2 runtime candidate while preserving zero decisions."""

    expectations = {
        RUNTIME_INVENTORY: EXPECTED_RUNTIME_INVENTORY_SHA256,
        RUNTIME_SOURCE_GATE: EXPECTED_RUNTIME_SOURCE_GATE_SHA256,
        RUNTIME_REVIEW_ITEM: EXPECTED_RUNTIME_ITEM_SHA256,
        RUNTIME_REVIEW_CONTRACT: EXPECTED_RUNTIME_CONTRACT_SHA256,
        RUNTIME_BLANK_RESPONSE: EXPECTED_RUNTIME_BLANK_SHA256,
        RUNTIME_ADOPTION_DECISION: EXPECTED_RUNTIME_DECISION_SHA256,
    }
    errors: list[str] = []
    documents: dict[Path, dict[str, Any]] = {}
    for relative, expected_sha in expectations.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"runtime review file is missing: {relative.as_posix()}")
            continue
        raw = path.read_bytes()
        if _repository_text_sha256(raw) != expected_sha:
            errors.append(f"runtime review file hash changed: {relative.as_posix()}")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            errors.append(f"runtime review file must be UTF-8 JSON: {relative.as_posix()}")
            continue
        if not isinstance(value, dict):
            errors.append(f"runtime review file must be a JSON object: {relative.as_posix()}")
            continue
        documents[relative] = value

    inventory = documents.get(RUNTIME_INVENTORY)
    if inventory is not None:
        if inventory.get("candidate_id") != (
            "CPYTHON-3.12.10-UV-0.10.7-TORCH-2.13.0-CPU-WINDOWS-X64-001"
        ):
            errors.append("runtime candidate identity changed")
        for field, expected in {
            "adopted": False,
            "downloaded_runtime_artifacts": 0,
            "installed_packages": 0,
            "executed_candidate_imports": 0,
            "scientific_work_started": False,
        }.items():
            if inventory.get(field) != expected:
                errors.append(f"runtime inventory {field} must equal {expected!r}")
        resolution = inventory.get("package_resolution")
        if not isinstance(resolution, dict) or resolution.get(
            "effective_windows_packages"
        ) != 20:
            errors.append("runtime inventory must bind 20 effective Windows packages")
        private = inventory.get("private_resolution_inputs")
        if not isinstance(private, dict) or private.get("lock_sha256") != (
            "66ef4a354db2a1e51bd6ebeca81844c1f71497c1f8164e27b99816da5ce2e081"
        ):
            errors.append("runtime private lock identity changed")

    source_gate = documents.get(RUNTIME_SOURCE_GATE)
    if source_gate is not None:
        decision = source_gate.get("decision")
        if not isinstance(decision, dict) or decision.get("status") != "ready":
            errors.append("runtime source gate must remain ready for owner review")
        scope = source_gate.get("scope_dispositions")
        if not isinstance(scope, dict) or scope.get("download_install_or_execute") != (
            "blocked_until_explicit_M2_U003_yes"
        ):
            errors.append("runtime source gate must block adoption until explicit yes")

    expected_binding = {
        "item_id": EXPECTED_RUNTIME_ITEM_ID,
        "evidence_sha256": EXPECTED_RUNTIME_INVENTORY_SHA256,
    }
    item = documents.get(RUNTIME_REVIEW_ITEM)
    if item is not None:
        if item.get("template") is not False:
            errors.append("runtime review item template must be false")
        if item.get("review_id") != EXPECTED_RUNTIME_REVIEW_ID:
            errors.append("runtime review item review_id changed")
        if item.get("item_id") != EXPECTED_RUNTIME_ITEM_ID:
            errors.append("runtime review item item_id changed")
        if item.get("evidence_sha256") != EXPECTED_RUNTIME_INVENTORY_SHA256:
            errors.append("runtime review item inventory binding changed")
        if set(item.get("allowed_decisions", {})) != {"yes", "no"}:
            errors.append("runtime review item must define only yes/no decisions")

    contract = documents.get(RUNTIME_REVIEW_CONTRACT)
    if contract is not None:
        if contract.get("template") is not False:
            errors.append("runtime review contract template must be false")
        if contract.get("review_id") != EXPECTED_RUNTIME_REVIEW_ID:
            errors.append("runtime review contract review_id changed")
        if contract.get("allowed_decisions") != ["yes", "no"]:
            errors.append("runtime review contract decisions must be yes/no")
        if contract.get("required_attestation") is not True:
            errors.append("runtime review contract must require attestation")
        if contract.get("items") != [expected_binding]:
            errors.append("runtime review contract item binding changed")

    blank = documents.get(RUNTIME_BLANK_RESPONSE)
    if blank is not None:
        expected_response = dict(expected_binding, decision=None, notes="")
        if blank.get("review_id") != EXPECTED_RUNTIME_REVIEW_ID:
            errors.append("runtime blank response review_id changed")
        if blank.get("completed") is not False:
            errors.append("runtime blank response must remain incomplete")
        if blank.get("review_started_at_utc") is not None or blank.get(
            "review_completed_at_utc"
        ) is not None:
            errors.append("runtime blank response timestamps must remain null")
        if blank.get("reviewer") != {"attestation": False}:
            errors.append("runtime blank response attestation must remain false")
        if blank.get("responses") != [expected_response]:
            errors.append("runtime blank response must contain zero decisions")

    resolved = documents.get(RUNTIME_ADOPTION_DECISION)
    if resolved is not None:
        if resolved.get("review_id") != EXPECTED_RUNTIME_REVIEW_ID:
            errors.append("runtime adoption decision review_id changed")
        if resolved.get("decision") != "yes":
            errors.append("runtime adoption decision must equal yes")
        aggregate = resolved.get("aggregate")
        if not isinstance(aggregate, dict) or any(
            aggregate.get(key) != value
            for key, value in {
                "expected_decisions": 1,
                "received_decisions": 1,
                "yes": 1,
                "no": 0,
                "ambiguous": 0,
                "missing": 0,
                "attestation_satisfied": True,
                "exact_bundle_match": True,
                "human_decisions_fabricated": False,
            }.items()
        ):
            errors.append("runtime adoption aggregate is inconsistent")
        locked = resolved.get("locked_review_evidence")
        if not isinstance(locked, dict) or locked.get(
            "raw_response_or_notes_committed"
        ) is not False:
            errors.append("runtime raw response and notes must remain private")
        candidate = resolved.get("candidate_identity")
        if not isinstance(candidate, dict) or candidate.get("inventory_sha256") != (
            EXPECTED_RUNTIME_INVENTORY_SHA256
        ):
            errors.append("runtime adoption decision candidate binding changed")

    milestone_path = root / SYNTHETIC_PREFLIGHT_MILESTONE
    if milestone_path.is_file():
        try:
            milestone = json.loads(milestone_path.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            milestone = None
        if isinstance(milestone, dict):
            gates = milestone.get("human_gates")
            selected = [
                gate
                for gate in gates or []
                if isinstance(gate, dict)
                and gate.get("id") == "M2-GATE-DEPENDENCY-RUNTIME"
            ]
            if len(selected) != 1 or selected[0].get("status") != "passed":
                errors.append("M2 runtime gate must record the resolved pass")
            elif selected[0].get("review_preparation", {}).get(
                "human_decisions_created"
            ) != 1:
                errors.append("M2 runtime review must record one human decision")

    return errors


def check_runtime_failure_and_successor_review(root: Path) -> list[str]:
    """Retain candidate 001 failure and keep candidate 002 exact and unadopted."""

    expectations = {
        RUNTIME_ACTIVATION_FAILURE: EXPECTED_RUNTIME_FAILURE_SHA256,
        RUNTIME_SUCCESSOR_INVENTORY: EXPECTED_RUNTIME_SUCCESSOR_INVENTORY_SHA256,
        RUNTIME_SUCCESSOR_SOURCE_GATE: EXPECTED_RUNTIME_SUCCESSOR_SOURCE_GATE_SHA256,
        RUNTIME_SUCCESSOR_REVIEW_ITEM: EXPECTED_RUNTIME_SUCCESSOR_ITEM_SHA256,
        RUNTIME_SUCCESSOR_REVIEW_CONTRACT: EXPECTED_RUNTIME_SUCCESSOR_CONTRACT_SHA256,
        RUNTIME_SUCCESSOR_BLANK_RESPONSE: EXPECTED_RUNTIME_SUCCESSOR_BLANK_SHA256,
        RUNTIME_SUCCESSOR_ADOPTION_DECISION: EXPECTED_RUNTIME_SUCCESSOR_DECISION_SHA256,
        RUNTIME_SUCCESSOR_ACTIVATION: EXPECTED_RUNTIME_SUCCESSOR_ACTIVATION_SHA256,
    }
    errors: list[str] = []
    documents: dict[Path, dict[str, Any]] = {}
    for relative, expected_sha in expectations.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"runtime successor file is missing: {relative.as_posix()}")
            continue
        raw = path.read_bytes()
        if _repository_text_sha256(raw) != expected_sha:
            errors.append(f"runtime successor file hash changed: {relative.as_posix()}")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            errors.append(f"runtime successor file must be UTF-8 JSON: {relative.as_posix()}")
            continue
        if not isinstance(value, dict):
            errors.append(f"runtime successor file must be a JSON object: {relative.as_posix()}")
            continue
        documents[relative] = value

    failure = documents.get(RUNTIME_ACTIVATION_FAILURE)
    if failure is not None:
        if failure.get("disposition") != "fail" or failure.get("route_status") != "closed_on_this_host":
            errors.append("runtime candidate 001 must remain failed and closed")
        attempt = failure.get("attempt")
        if not isinstance(attempt, dict) or any(
            attempt.get(key) != expected
            for key, expected in {
                "process_exit_code": 0,
                "target_python_present": False,
                "installer_action": "Modify",
                "package_sync_started": False,
                "wheels_downloaded": 0,
                "candidate_imports_executed": 0,
            }.items()
        ):
            errors.append("runtime candidate 001 failure facts changed")
        recovery = failure.get("recovery")
        if not isinstance(recovery, dict) or recovery.get("status") != "pass":
            errors.append("runtime candidate 001 recovery status must remain scoped pass")
        scientific = failure.get("scientific_boundary")
        if not isinstance(scientific, dict) or any(
            scientific.get(key) != expected
            for key, expected in {
                "synthetic_preflight_started": False,
                "benchmark_accessed": False,
                "training_runs": 0,
                "checkpoints": 0,
                "inference_runs": 0,
                "evaluations": 0,
            }.items()
        ):
            errors.append("runtime activation failure must preserve zero scientific work")

    inventory = documents.get(RUNTIME_SUCCESSOR_INVENTORY)
    if inventory is not None:
        if inventory.get("candidate_id") != "CPYTHON-3.12.10-EMBED-UV-0.10.7-TORCH-2.13.0-CPU-WINDOWS-X64-002":
            errors.append("runtime successor identity changed")
        for field, expected in {
            "adopted": False,
            "downloaded_runtime_artifacts": 0,
            "installed_packages": 0,
            "executed_candidate_imports": 0,
            "scientific_work_started": False,
        }.items():
            if inventory.get(field) != expected:
                errors.append(f"runtime successor inventory {field} must equal {expected!r}")
        python_record = inventory.get("python")
        if not isinstance(python_record, dict) or python_record.get("artifact_sha256") != "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3":
            errors.append("runtime successor embeddable ZIP identity changed")
        package_plan = inventory.get("package_plan")
        if not isinstance(package_plan, dict) or package_plan.get("private_lock_sha256") != "66ef4a354db2a1e51bd6ebeca81844c1f71497c1f8164e27b99816da5ce2e081":
            errors.append("runtime successor must retain the exact wheel lock")

    source_gate = documents.get(RUNTIME_SUCCESSOR_SOURCE_GATE)
    if source_gate is not None:
        decision = source_gate.get("decision")
        if not isinstance(decision, dict) or decision.get("status") != "ready":
            errors.append("runtime successor source gate must remain ready")
        scope = source_gate.get("scope_dispositions")
        if not isinstance(scope, dict) or scope.get("download_extract_vendor_or_execute") != "blocked_until_explicit_M2_U004C_yes":
            errors.append("runtime successor source gate must block activation until exact yes")

    expected_binding = {
        "item_id": EXPECTED_RUNTIME_SUCCESSOR_ITEM_ID,
        "evidence_sha256": EXPECTED_RUNTIME_SUCCESSOR_INVENTORY_SHA256,
    }
    item = documents.get(RUNTIME_SUCCESSOR_REVIEW_ITEM)
    if item is not None:
        if item.get("review_id") != EXPECTED_RUNTIME_SUCCESSOR_REVIEW_ID or item.get("item_id") != EXPECTED_RUNTIME_SUCCESSOR_ITEM_ID or item.get("evidence_sha256") != EXPECTED_RUNTIME_SUCCESSOR_INVENTORY_SHA256:
            errors.append("runtime successor review item binding changed")
        if set(item.get("allowed_decisions", {})) != {"yes", "no"}:
            errors.append("runtime successor review must define only yes/no")

    contract = documents.get(RUNTIME_SUCCESSOR_REVIEW_CONTRACT)
    if contract is not None:
        if contract.get("review_id") != EXPECTED_RUNTIME_SUCCESSOR_REVIEW_ID or contract.get("items") != [expected_binding] or contract.get("allowed_decisions") != ["yes", "no"] or contract.get("required_attestation") is not True:
            errors.append("runtime successor review contract changed")

    blank = documents.get(RUNTIME_SUCCESSOR_BLANK_RESPONSE)
    if blank is not None:
        expected_response = dict(expected_binding, decision=None, notes="")
        if blank.get("review_id") != EXPECTED_RUNTIME_SUCCESSOR_REVIEW_ID or blank.get("completed") is not False or blank.get("reviewer") != {"attestation": False} or blank.get("responses") != [expected_response]:
            errors.append("runtime successor blank response must contain zero decisions")

    decision_record = documents.get(RUNTIME_SUCCESSOR_ADOPTION_DECISION)
    if decision_record is not None:
        if decision_record.get("review_id") != EXPECTED_RUNTIME_SUCCESSOR_REVIEW_ID or decision_record.get("decision") != "yes":
            errors.append("runtime successor adoption decision changed")
        aggregate = decision_record.get("aggregate")
        if not isinstance(aggregate, dict) or any(
            aggregate.get(key) != value
            for key, value in {
                "expected_decisions": 1,
                "received_decisions": 1,
                "yes": 1,
                "no": 0,
                "ambiguous": 0,
                "missing": 0,
                "attestation_satisfied": True,
                "exact_bundle_match": True,
                "human_decisions_fabricated": False,
            }.items()
        ):
            errors.append("runtime successor adoption aggregate is inconsistent")
        locked = decision_record.get("locked_review_evidence")
        if not isinstance(locked, dict) or locked.get("raw_response_or_notes_committed") is not False:
            errors.append("runtime successor raw response and notes must remain private")

    activation = documents.get(RUNTIME_SUCCESSOR_ACTIVATION)
    if activation is not None:
        if activation.get("disposition") != "pass" or activation.get("decision_sha256") != EXPECTED_RUNTIME_SUCCESSOR_DECISION_SHA256:
            errors.append("runtime successor activation disposition or decision binding changed")
        installed = activation.get("package_installation")
        if not isinstance(installed, dict) or installed.get("installed_package_count") != 20 or installed.get("private_uv_lock_sha256") != "66ef4a354db2a1e51bd6ebeca81844c1f71497c1f8164e27b99816da5ce2e081":
            errors.append("runtime successor activation lock or package count changed")
        checks = activation.get("activation_checks")
        if not isinstance(checks, dict) or any(
            checks.get(key) is not True
            for key in ("rasterio_memoryfile_geotiff_roundtrip", "fresh_process_replay_exact_match", "safe_weights_only_reload")
        ) or checks.get("cuda_available") is not False:
            errors.append("runtime successor activation checks changed")
        scientific = activation.get("scientific_boundary")
        if not isinstance(scientific, dict) or any(scientific.get(key) != 0 for key in ("training_runs", "checkpoints", "inference_runs", "evaluations")) or scientific.get("benchmark_accessed") is not False or scientific.get("model_implementation_started") is not False:
            errors.append("runtime successor activation must preserve zero scientific/model work")

    milestone_path = root / SYNTHETIC_PREFLIGHT_MILESTONE
    if milestone_path.is_file():
        try:
            milestone = json.loads(milestone_path.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            milestone = None
        if isinstance(milestone, dict):
            units = {unit.get("id"): unit for unit in milestone.get("units", []) if isinstance(unit, dict)}
            failed = units.get("M2-U004-LOCKED-RUNTIME-ACTIVATION", {})
            successor = units.get("M2-U004C-RUNTIME-SUCCESSOR-ADOPTION-DECISION", {})
            if failed.get("status") != "failed" or failed.get("disposition") != "remediate":
                errors.append("M2 must retain candidate 001 activation as failed with remediation disposition")
            activated = units.get("M2-U004D-LOCKED-RUNTIME-SUCCESSOR-ACTIVATION", {})
            model_unit = units.get("M2-U005-MODEL-AND-PACKAGING-IMPLEMENTATION", {})
            if successor.get("status") != "complete" or successor.get("disposition") != "pass" or successor.get("human_gate") is not True:
                errors.append("M2 successor decision must record the resolved pass")
            if activated.get("status") != "complete" or activated.get("disposition") != "pass":
                errors.append("M2 successor activation must record complete pass")
            lifecycle_unit = units.get("M2-U006-SYNTHETIC-LIFECYCLE-EXECUTION", {})
            verification_unit = units.get("M2-U007-INTEGRATED-VERIFICATION", {})
            if model_unit.get("status") != "complete" or model_unit.get("disposition") != "pass":
                errors.append("M2 model implementation must record complete pass")
            if lifecycle_unit.get("status") != "complete" or lifecycle_unit.get("disposition") != "pass":
                errors.append("M2 synthetic lifecycle must record complete pass")
            publication_unit = units.get("M2-U008-REVIEWED-PR-VERIFICATION", {})
            if verification_unit.get("status") != "complete" or verification_unit.get("disposition") != "pass":
                errors.append("M2 integrated verification must record complete pass")
            if publication_unit.get("status") != "complete" or publication_unit.get("disposition") != "pass":
                errors.append("M2 reviewed publication must remain a completed pass")
            gates = [gate for gate in milestone.get("human_gates", []) if isinstance(gate, dict) and gate.get("id") == "M2-GATE-DEPENDENCY-RUNTIME-SUCCESSOR"]
            if len(gates) != 1 or gates[0].get("status") != "passed" or gates[0].get("review_preparation", {}).get("human_decisions_created") != 1:
                errors.append("M2 successor gate must record one resolved human decision")

    return errors


def check_synthetic_preflight_record(root: Path) -> list[str]:
    """Bind the fixed source and synthetic-only replay evidence without importing torch."""

    errors: list[str] = []
    record_path = root / SYNTHETIC_PREFLIGHT_RECORD
    if not record_path.is_file():
        return ["synthetic preflight record is missing"]
    raw = record_path.read_bytes()
    if _repository_text_sha256(raw) != EXPECTED_SYNTHETIC_PREFLIGHT_RECORD_SHA256:
        errors.append("synthetic preflight record hash changed")
    try:
        record = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return errors + ["synthetic preflight record must be UTF-8 JSON"]
    if record.get("disposition") != "pass" or record.get("scope") != "wholly_synthetic_engineering_evidence_only":
        errors.append("synthetic preflight disposition or scope changed")
    if record.get("benchmark_accessed") is not False or record.get("scientific_output") is not False:
        errors.append("synthetic preflight must remain benchmark-free and non-scientific")
    implementation = record.get("implementation")
    if not isinstance(implementation, dict) or implementation.get("architecture_id") != "burnlens-exp3-pointwise-6x8x8x1-v1" or implementation.get("parameter_count") != 137:
        errors.append("synthetic model architecture identity changed")
    declared_sources = {
        Path(item.get("path")): item
        for item in implementation.get("source_files", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    } if isinstance(implementation, dict) else {}
    if set(declared_sources) != set(SYNTHETIC_SOURCE_IDENTITIES):
        errors.append("synthetic source roster changed")
    for relative, expected_sha in SYNTHETIC_SOURCE_IDENTITIES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"synthetic source missing: {relative.as_posix()}")
            continue
        raw_source = path.read_bytes()
        if _repository_text_sha256(raw_source) != expected_sha:
            errors.append(f"synthetic source hash changed: {relative.as_posix()}")
        declared = declared_sources.get(relative)
        if not isinstance(declared, dict) or declared.get("sha256") != expected_sha:
            errors.append(f"synthetic record source binding changed: {relative.as_posix()}")
    for role in ("primary_execution", "independent_replay"):
        value = record.get(role)
        if not isinstance(value, dict) or value.get("files") != 7 or value.get("bytes") != 20628 or value.get("roster_sha256") != "9c008f10e73d6829710fabce0a20de500e6b403a6f807c9a3cb45222555913f3" or value.get("receipt_sha256") != "7a3fde9902b528f3c5457eaf9a12c2c8444f9de5f6fb88ed07bddc97bded7b28":
            errors.append(f"synthetic {role} binding changed")
    deterministic = record.get("deterministic_evidence")
    if not isinstance(deterministic, dict) or deterministic.get("fingerprint") != "d13ec92fc783300cd56730e7ce050b88d2f2fc03ce3d805fcae8485ecffbd607" or any(
        deterministic.get(key) is not True
        for key in (
            "loss_decreased",
            "finite_nonzero_gradients",
            "initial_and_final_weights_differ",
            "fresh_process_logits_exact",
            "fresh_process_probabilities_exact",
            "checkpoint_tensor_state_exact",
            "primary_and_replay_checkpoint_bytes_exact",
            "primary_and_replay_geotiff_bytes_exact",
            "primary_and_replay_render_bytes_exact",
            "primary_and_replay_history_bytes_exact",
        )
    ):
        errors.append("synthetic deterministic evidence changed")
    gates = record.get("gates")
    if not isinstance(gates, dict) or any(value != "pass" for value in gates.values()):
        errors.append("synthetic preflight gates must all pass")
    return errors


def check_checkout_portability(root: Path) -> list[str]:
    """Require hash-bound repository text to retain LF bytes on every checkout."""

    path = root / ".gitattributes"
    if not path.is_file():
        return ["missing LF checkout policy: .gitattributes"]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [f"invalid LF checkout policy: {exc}"]
    if "* text=auto eol=lf" not in lines:
        return [".gitattributes must enforce LF for repository text"]
    return []


def check_frozen_protocol_record(root: Path) -> list[str]:
    """Bind the complete M3 protocol without loading benchmark arrays."""

    errors: list[str] = []
    protocol_path = root / FROZEN_PROTOCOL
    record_path = root / PROTOCOL_FREEZE_RECORD
    if not protocol_path.is_file() or not record_path.is_file():
        return errors
    protocol_raw = protocol_path.read_bytes()
    record_raw = record_path.read_bytes()
    if _repository_text_sha256(protocol_raw) != EXPECTED_FROZEN_PROTOCOL_SHA256:
        errors.append("frozen protocol hash changed")
    if _repository_text_sha256(record_raw) != EXPECTED_PROTOCOL_FREEZE_RECORD_SHA256:
        errors.append("protocol freeze record hash changed")
    try:
        protocol = json.loads(protocol_raw.decode("utf-8"))
        record = json.loads(record_raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return errors + ["protocol and freeze record must be UTF-8 JSON"]
    if protocol.get("status") != "frozen" or protocol.get("protocol_id") != (
        "EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001"
    ):
        errors.append("protocol identity or frozen status changed")
    model = protocol.get("model")
    if not isinstance(model, dict) or model.get("trainable_parameters") != 137:
        errors.append("frozen protocol model identity changed")
    execution = protocol.get("execution")
    if not isinstance(execution, dict) or execution.get("seeds") != [
        20260725,
        20260726,
        20260727,
    ]:
        errors.append("frozen protocol seed roster changed")
    roles = protocol.get("data", {}).get("roles", {})
    if not isinstance(roles, dict) or any(
        len(roles.get(role, {}).get("patch_ids", [])) != 4
        for role in ("train", "validation", "test")
    ):
        errors.append("frozen protocol role roster changed")
    if record.get("disposition") != "pass_accepted" or record.get(
        "acceptance_state"
    ) != "accepted_live_main":
        errors.append("protocol freeze accepted state changed")
    acceptance = record.get("acceptance")
    if not isinstance(acceptance, dict) or acceptance.get("live_main_commit") != (
        "10bc499db09bccd66e3bc9289d655ab561bec857"
    ) or acceptance.get("candidate_and_live_tree") != (
        "65d3fcb5b01b5f8448ab863a873a76d1c8da51ee"
    ) or acceptance.get("merge_ci") != 32689530033:
        errors.append("protocol freeze live acceptance receipt changed")
    boundary = record.get("scientific_boundary")
    if not isinstance(boundary, dict) or boundary.get("test_values_opened") is not False:
        errors.append("protocol freeze must retain unopened test values")
    elif any(
        boundary.get(field) != 0
        for field in (
            "benchmark_arrays_loaded",
            "training_runs",
            "checkpoints",
            "inference_runs",
            "evaluations",
            "releases",
        )
    ):
        errors.append("protocol freeze must preserve zero scientific outputs")
    return errors


def check_frozen_training_record(root: Path) -> list[str]:
    """Bind M4 train/validation evidence without reading external run bytes."""

    errors: list[str] = []
    data_path = root / TRAIN_VALIDATION_DATA_RECORD
    training_path = root / FROZEN_TRAINING_RECORD
    if not data_path.is_file() or not training_path.is_file():
        return errors
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        training = json.loads(training_path.read_text(encoding="utf-8"))
        profile = json.loads(
            (root / MILESTONE_FOUR_CONTROL_PROFILE).read_text(encoding="utf-8")
        )
        milestone = json.loads(
            (root / FROZEN_TRAINING_MILESTONE).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M4 data, training, profile, and milestone records must be UTF-8 JSON"]

    if data.get("disposition") != "pass" or data.get("protocol_sha256") != (
        EXPECTED_FROZEN_PROTOCOL_SHA256
    ):
        errors.append("M4 train/validation data disposition or protocol binding changed")
    receipt = data.get("external_receipt", {})
    if receipt != {
        "path": "C:\\Projects\\Active\\burnlens-experiment-three-custody\\training\\m4-data-verification-001.json",
        "bytes": 9363,
        "sha256": "bec3084c91c98d9cdd49ba1b1aec96d7f6a77cf54441edc988503ee6138e2b2a",
    }:
        errors.append("M4 train/validation external receipt binding changed")
    verified = data.get("verified", {})
    if any(
        verified.get(key) != value
        for key, value in {
            "roles_decoded": ["train", "validation"],
            "arrays": 32,
            "bytes": 888832,
            "all_manifest_hashes_match": True,
            "all_dtypes_shapes_masks_match": True,
            "normalized_values_finite": True,
        }.items()
    ):
        errors.append("M4 train/validation verification summary changed")
    data_boundary = data.get("boundary", {})
    if data_boundary.get("test_values_opened") is not False or data_boundary.get(
        "test_arrays_listed_or_decoded"
    ) != 0:
        errors.append("M4 data gate must preserve zero test access")

    if training.get("record_id") != "EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001" or training.get(
        "disposition"
    ) != "pass" or training.get("scope") != "frozen_train_validation_lifecycle_only":
        errors.append("M4 frozen-training identity, scope, or disposition changed")
    if training.get("protocol", {}).get("canonical_lf_sha256") != (
        EXPECTED_FROZEN_PROTOCOL_SHA256
    ):
        errors.append("M4 frozen-training protocol binding changed")

    observed_bindings = {
        Path(item.get("path", "")): item.get("sha256")
        for item in training.get("source_bindings", [])
        if isinstance(item, dict)
    }
    if observed_bindings != FROZEN_TRAINING_SOURCE_IDENTITIES:
        errors.append("M4 frozen-training source roster changed")
    for relative, expected_sha in FROZEN_TRAINING_SOURCE_IDENTITIES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"M4 frozen-training source missing: {relative.as_posix()}")
        elif _repository_text_sha256(path.read_bytes()) != expected_sha:
            errors.append(f"M4 frozen-training source hash changed: {relative.as_posix()}")

    attempt = training.get("accepted_attempt", {})
    each_root = attempt.get("each_root", {})
    if any(
        attempt.get(key) != value
        for key, value in {
            "attempt_id": "m4-2026-005",
            "primary_replay_exact": True,
            "milestone_4_artifact_schema_exact": True,
            "test_values_opened": False,
            "test_arrays_listed_or_decoded": 0,
        }.items()
    ) or any(
        each_root.get(key) != value
        for key, value in {
            "files_including_receipt": 20,
            "bytes_including_receipt": 270793,
            "exact_replay_receipt_sha256": "75c2263e6c3672ad18e603f964982a1bede2c3652b45be4bbd1b0b51d159bf4b",
            "payload_files": 19,
            "payload_bytes": 266578,
            "payload_roster_sha256": "e3115254c1602e9f1c0aba7e91c7d1c2984db106053a880afbc069f6beb82473",
            "per_seed_artifacts": ["run-manifest.json", "training-history.json", "selected-checkpoint/manifest.json", "selected-checkpoint/weights.pt", "validation-probabilities.npz", "replay-receipt.json"],
            "aggregate_artifacts_present": ["shared-threshold-selection.json", "exact-replay-receipt.json"],
        }.items()
    ):
        errors.append("M4 accepted attempt identity or exact-replay receipt changed")
    timing = training.get("execution_timing_observation", {})
    if timing.get("method") != (
        "Controller UTC wall clock and monotonic stopwatch; excluded from deterministic run roots"
    ) or any(
        timing.get(role, {}).get("exit_code") != 0
        or not isinstance(timing.get(role, {}).get("duration_seconds"), (int, float))
        or timing.get(role, {}).get("duration_seconds", 0) <= 0
        for role in ("primary", "replay")
    ):
        errors.append("M4 execution timing observation changed or is incomplete")

    expected_seeds = [
        (20260725, 130, 105, 0.6794654130935669, "50477e8f2be155e042816735bade3664bf318e2ce46e34032a4132911266b2fd"),
        (20260726, 172, 147, 0.6747468709945679, "19b0308c13779d2b92c6931f5e8a4b409f83c910a9c7933abe757a0fe03132a2"),
        (20260727, 171, 146, 0.6462924480438232, "078d4ffc648e00aeece354b7a214b6df3afb6d259c12ef5c788b8c4f7bdfe56c"),
    ]
    seeds = training.get("seeds", [])
    observed_seeds = [
        (
            item.get("seed"),
            item.get("epochs_completed"),
            item.get("selected_epoch"),
            item.get("selected_validation_balanced_bce"),
            item.get("selected_tensor_state_sha256"),
        )
        for item in seeds
        if isinstance(item, dict)
    ]
    if observed_seeds != expected_seeds or any(
        not item.get("early_stopped")
        or not isinstance(item.get("first_gradient_norm"), (int, float))
        or item.get("first_gradient_norm", 0) <= 0
        or item.get("initial_tensor_state_sha256") == item.get("first_step_tensor_state_sha256")
        or item.get("weights_bytes") != 3285
        for item in seeds
        if isinstance(item, dict)
    ):
        errors.append("M4 per-seed training, gradient, selection, or checkpoint evidence changed")

    threshold = training.get("shared_validation_threshold", {})
    if threshold != {
        "selected_threshold": 0.5,
        "minimum_seed_event_macro_dice": 0.3333333333333333,
        "median_seed_event_class_macro_iou": 0.625,
        "selection_scope": "validation_only",
        "test_values_opened": False,
    }:
        errors.append("M4 shared validation threshold evidence changed")
    retained = training.get("retained_attempts", [])
    if [(item.get("attempt_id"), item.get("disposition")) for item in retained] != [
        ("m4-2026-001-primary", "fail"),
        ("m4-2026-002", "invalid"),
        ("m4-2026-003", "invalid"),
        ("m4-2026-004", "invalid"),
    ]:
        errors.append("M4 failed/invalid attempt retention changed")
    verification = training.get("verification", {})
    required_passes = (
        "all_gradients_finite_nonzero",
        "all_first_steps_changed_weights",
        "all_histories_complete",
        "all_checkpoints_selected_by_frozen_rule",
        "all_checkpoints_tensor_only_weights_pt",
        "all_fresh_process_reloads_exact",
        "all_validation_probability_packages_exact",
        "shared_threshold_recomputed_exact",
        "primary_replay_exact",
        "all_seeds_trained_in_fresh_isolated_processes",
        "runtime_identity_exact",
        "exceptions_null",
    )
    if any(verification.get(key) is not True for key in required_passes) or verification.get(
        "test_values_opened"
    ) is not False:
        errors.append("M4 frozen-training verification gates changed")

    expected_outputs = {
        "datasets": 1,
        "training_runs": 3,
        "checkpoints": 3,
        "inference_runs": 3,
        "evaluations": 0,
        "releases": 0,
    }
    if training.get("scientific_outputs") != expected_outputs or profile.get(
        "scientific_outputs"
    ) != expected_outputs or milestone.get("scientific_outputs") != expected_outputs:
        errors.append("M4 scientific output counts are not aligned")
    if profile.get("scientific_state") != "trained_validation_selected_candidate":
        errors.append("M4 profile scientific state changed")
    exits = {item.get("id"): item.get("status") for item in milestone.get("exit_conditions", [])}
    for exit_id in (
        "EXIT-M4-DATA",
        "EXIT-M4-RUNS",
        "EXIT-M4-RELOAD",
        "EXIT-M4-THRESHOLD",
        "EXIT-M4-REPLAY",
        "EXIT-M4-TEST-SEALED",
    ):
        if exits.get(exit_id) != "pass":
            errors.append(f"{exit_id} must pass in the M4 candidate")
    if exits.get("EXIT-M4-VERIFIED-CHECKPOINT") != "pass":
        errors.append("M4 live checkpoint acceptance must remain passed")
    units = {item.get("id"): item.get("status") for item in milestone.get("units", [])}
    if any(units.get(unit_id) != "complete" for unit_id in (
        "M4-U003-IMPLEMENTATION",
        "M4-U004-THREE-SEED-EXECUTION",
        "M4-U005-REPLAY-VERIFY",
    )) or units.get("M4-U006-REVIEWED-PR") != "complete":
        errors.append("M4 unit status does not match the accepted live checkpoint")
    return errors


def check_preopening_audit(root: Path) -> list[str]:
    """Bind the metadata-only M5 audit and retain zero-value access."""

    record_path = root / PREOPENING_AUDIT
    verifier_path = root / PREOPENING_VERIFIER
    if not record_path.is_file() or not verifier_path.is_file():
        return []
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M5 pre-opening audit must be UTF-8 JSON"]
    errors: list[str] = []
    if record.get("record_id") != "EXPERIMENT-THREE-M5-PREOPENING-AUDIT-2026-001" or record.get("disposition") != "pass":
        errors.append("M5 pre-opening audit identity or disposition changed")
    verification = record.get("identity_verification", {})
    expected_verifier = {
        "path": PREOPENING_VERIFIER.as_posix(),
        "bytes": 4580,
        "sha256": "894df7525aea10845920d51582c7f4650b14cab8a2877ec74df0b814379724f2",
    }
    if verification.get("verifier") != expected_verifier:
        errors.append("M5 pre-opening verifier binding changed")
    elif verifier_path.stat().st_size != 4580 or _repository_text_sha256(verifier_path.read_bytes()) != expected_verifier["sha256"]:
        errors.append("M5 pre-opening verifier source changed")
    expected_groups = {
        "binding_record": (3, 70314, "19973be5c98d1c7a246dfbd4e89af1018b95e89b008a5d9857ffe92807ff4839"),
        "rbr_comparator_record": (1, 21257, "05ceda96f8d756f5b6d9d8b11e2a41ccb8923868814c436cd210d7c9f5b3ffbb"),
        "test_dataset_arrays": (16, 444416, "04061c6a6747421e2cb4afbc079f2611c22ec6944c0839391c2b6a1611275321"),
        "unet_comparator_record": (1, 26268, "449cf35b0c51ed43dc3d2adae6dc9b35758880c8625d8d68c415d5b2736fee6a"),
        "unet_test_arrays": (8, 82944, "1c6bbd067273a5b1526aac0bfd7f43a92db36ef9259632da1b46840b5b0467d1"),
    }
    groups = verification.get("groups", {})
    for name, expected in expected_groups.items():
        observed = groups.get(name, {})
        if (observed.get("files"), observed.get("bytes"), observed.get("roster_sha256")) != expected or observed.get("mismatches") != 0:
            errors.append(f"M5 pre-opening roster changed: {name}")
    if any(verification.get(field) != value for field, value in {
        "arrays_deserialized": 0,
        "values_decoded": 0,
        "numpy_imported": False,
    }.items()):
        errors.append("M5 pre-opening audit must retain zero decoded values")
    boundary = record.get("boundary", {})
    expected_zero = (
        "test_arrays_deserialized",
        "historical_prediction_arrays_deserialized",
        "evaluation_roots_created",
        "evaluations",
        "scientific_choices_made",
    )
    if boundary.get("test_values_opened") is not False or boundary.get("historical_prediction_values_opened") is not False or any(boundary.get(field) != 0 for field in expected_zero):
        errors.append("M5 pre-opening boundary changed")
    opening = record.get("one_opening_design", {})
    if opening.get("preopening_state") != "absent" or opening.get("opening_marker_exists") is not False or opening.get("terminal_package_exists") is not False:
        errors.append("M5 opening state must remain sealed before U003")
    return errors


def check_evaluation_path_preflight(root: Path) -> list[str]:
    """Bind the accepted fabricated M5 path and retained visual failure."""

    path = root / EVALUATION_PATH_PREFLIGHT
    if not path.is_file():
        return []
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M5 evaluation-path preflight must be UTF-8 JSON"]
    errors: list[str] = []
    if record.get("disposition") != "pass" or record.get("scope") != "wholly_fabricated_non_scientific_evaluation_path":
        errors.append("M5 evaluation-path preflight scope or disposition changed")
    bindings = {Path(item.get("path", "")): item.get("sha256") for item in record.get("source_bindings", []) if isinstance(item, dict)}
    if bindings != EVALUATION_PATH_SOURCES:
        errors.append("M5 evaluation-path source roster changed")
    for relative, expected_sha in EVALUATION_PATH_SOURCES.items():
        source = root / relative
        if not source.is_file() or _repository_text_sha256(source.read_bytes()) != expected_sha:
            errors.append(f"M5 evaluation-path source changed: {relative.as_posix()}")
    attempts = record.get("retained_attempts", [])
    if [(item.get("attempt_id"), item.get("disposition")) for item in attempts] != [("m5-u003-001", "fail")]:
        errors.append("M5 visual-failure retention changed")
    accepted = record.get("accepted_attempt", {})
    if any(accepted.get(key) != value for key, value in {
        "attempt_id": "m5-u003-002",
        "payload_files_each": 49,
        "payload_bytes_each": 92385,
        "payload_roster_sha256": "98dcec345c4b8d8876a05cac9babecf4aa04c1e269578243ad27fbfd78fe6135",
        "primary_replay_exact": True,
    }.items()):
        errors.append("M5 accepted fabricated replay identity changed")
    if accepted.get("geotiffs", {}).get("all_reopen_exact") is not True or accepted.get("render", {}).get("direct_visual_inspection") != "pass":
        errors.append("M5 geospatial or rendered proof changed")
    boundary = record.get("boundary", {})
    if boundary.get("benchmark_accessed") is not False or boundary.get("test_values_opened") is not False or boundary.get("historical_prediction_values_opened") is not False or boundary.get("evaluations") != 0:
        errors.append("M5 fabricated preflight must retain sealed scientific evidence")
    return errors


def check_retrospective_evaluation_record(root: Path) -> list[str]:
    """Bind the one M5 opening, frozen outcomes, exact replay, and output counts."""

    record_path = root / RETROSPECTIVE_EVALUATION_RECORD
    profile_path = root / MILESTONE_FIVE_CONTROL_PROFILE
    milestone_path = root / RETROSPECTIVE_EVALUATION_MILESTONE
    if not record_path.is_file() or not profile_path.is_file() or not milestone_path.is_file():
        return []
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        milestone = json.loads(milestone_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M5 retrospective evaluation control records must be UTF-8 JSON"]
    errors: list[str] = []
    if record.get("record_id") != "EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001" or record.get("scope") != "known_retrospective_sparse_prototype_core_compatibility":
        errors.append("M5 retrospective evaluation identity or scope changed")
    opening = record.get("opening", {})
    if any(opening.get(key) != value for key, value in {
        "opening_id": "M5-OPENING-2026-001",
        "previous_evaluation_roots": 0,
        "single_opening": True,
        "test_arrays_deserialized_once": 16,
        "historical_prediction_arrays_deserialized_once": 8,
        "post_test_changes": 0,
        "threshold": 0.5,
        "protocol_sha256": "12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e",
    }.items()):
        errors.append("M5 one-opening boundary changed")
    dispositions = record.get("dispositions", {})
    if dispositions.get("lifecycle_status") != "PASS" or dispositions.get("comparative_status") != "FAIL" or dispositions.get("no_tuning_or_rescue") is not True:
        errors.append("M5 lifecycle or comparative disposition changed")
    decision = record.get("decision_evidence", {})
    expected_decision = {
        "three_seed_median_event_class_macro_iou": 0.2201417004048583,
        "three_seed_median_worst_event_macro_dice": 0.29193899782135074,
        "strongest_constant_event_class_macro_iou": 0.28525641025641024,
        "strongest_constant_worst_event_macro_dice": 0.3333333333333333,
        "every_seed_every_event_nonconstant": False,
        "strictly_beats_constants_on_both": False,
    }
    if decision != expected_decision:
        errors.append("M5 frozen decision evidence changed")
    expected_seeds = [
        (20260725, 0.2201417004048583, 0.29193899782135074, False),
        (20260726, 0.20094760312151616, 0.11363636363636363, True),
        (20260727, 0.5794129720853859, 0.4652406417112299, True),
    ]
    observed_seeds = [
        (
            item.get("seed"),
            item.get("aggregate", {}).get("event_class_macro_iou"),
            item.get("aggregate", {}).get("worst_event_macro_dice"),
            item.get("aggregate", {}).get("all_events_nonconstant"),
        )
        for item in record.get("model_results", [])
        if isinstance(item, dict)
    ]
    if observed_seeds != expected_seeds or any(len(item.get("events", [])) != 2 for item in record.get("model_results", [])):
        errors.append("M5 per-seed or per-event result changed")
    comparators = record.get("comparators", {})
    expected_comparators = {
        "RBR": (1.0, 1.0, 0.43820224719101125, True),
        "canonical_experiment_one_unet": (0.21474358974358976, 0.2641509433962264, 1.0, False),
        "constant_background": (0.28525641025641024, 0.3333333333333333, 0.0, False),
        "constant_burned": (0.21474358974358976, 0.2641509433962264, 1.0, False),
    }
    observed_comparators = {
        name: (
            item.get("event_class_macro_iou"),
            item.get("worst_event_macro_dice"),
            item.get("predicted_burn_prevalence"),
            item.get("all_events_nonconstant"),
        )
        for name, item in comparators.items()
        if isinstance(item, dict)
    }
    if observed_comparators != expected_comparators:
        errors.append("M5 comparator result changed")
    package = record.get("external_package", {})
    payload = package.get("primary_and_replay", {})
    render = package.get("render", {})
    if any(package.get(key) != value for key, value in {"root_files": 108, "root_bytes": 747018}.items()) or any(payload.get(key) != value for key, value in {
        "files_each": 53,
        "bytes_each": 367150,
        "roster_sha256": "e322a10135243d06360393b21553602713285a0b2f7aeabbb924930073bd1d68",
        "exact": True,
    }.items()) or render.get("sha256") != "87d7653fcc39abb7d290a36daf1d6fa1372f46f092970a936c10024269ff96bf" or render.get("direct_visual_inspection") != "pass":
        errors.append("M5 terminal package or rendered identity changed")
    verification = record.get("independent_verification", {})
    if verification.get("status") != "PASS" or verification.get("checkpoint_reinference_exact") is not True or verification.get("metrics_recomputed_exact") is not True or verification.get("primary_replay_exact") is not True or verification.get("geotiffs_reopened") != 36 or verification.get("render_inspection") != "pass":
        errors.append("M5 independent verification changed")
    expected_outputs = {"datasets": 1, "training_runs": 3, "checkpoints": 3, "inference_runs": 6, "evaluations": 1, "releases": 0}
    if record.get("scientific_outputs") != expected_outputs or profile.get("scientific_outputs") != expected_outputs or milestone.get("scientific_outputs") != expected_outputs:
        errors.append("M5 scientific output counts are not aligned")
    if profile.get("scientific_state") != "evaluated_replay_verified_candidate":
        errors.append("M5 profile scientific state changed")
    units = {item.get("id"): item.get("status") for item in milestone.get("units", [])}
    if units.get("M5-U004-ONE-TIME-EVALUATION") != "complete" or units.get("M5-U005-INDEPENDENT-REPLAY") != "complete" or units.get("M5-U006-REVIEWED-PR") != "complete":
        errors.append("M5 unit state does not match the accepted checkpoint")
    exits = {item.get("id"): item.get("status") for item in milestone.get("exit_conditions", [])}
    for exit_id in ("EXIT-M5-ONE-OPENING", "EXIT-M5-ALL-SEEDS-CONTROLS", "EXIT-M5-GEOSPATIAL-RENDERED", "EXIT-M5-REPLAY", "EXIT-M5-DISPOSITIONS"):
        if exits.get(exit_id) != "pass":
            errors.append(f"{exit_id} must pass in the M5 candidate")
    if exits.get("EXIT-M5-VERIFIED-CHECKPOINT") != "pass":
        errors.append("M5 live checkpoint acceptance must remain passed")
    return errors


def check_reviewer_evidence_record(root: Path) -> list[str]:
    """Bind public-safe reviewer evidence and its no-controlled-byte boundary."""

    record_path = root / REVIEWER_EVIDENCE_RECORD
    manifest_path = root / PUBLIC_EVIDENCE_MANIFEST
    renderer_path = root / REVIEWER_RENDERER
    if not record_path.is_file() or not manifest_path.is_file() or not renderer_path.is_file():
        return []
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M6 reviewer evidence records must be UTF-8 JSON"]
    errors: list[str] = []
    if record.get("record_id") != "EXPERIMENT-THREE-M6-REVIEWER-EVIDENCE-2026-001" or record.get("status") != "PASS":
        errors.append("M6 reviewer evidence identity or status changed")
    renderer = record.get("renderer", {})
    if renderer != {"path": "scripts/render_reviewer_evidence.py", "bytes": 13411, "sha256": "c9dd1d33eedd11b15d690af85ddd52681c2895c5c76ee2eb53686a3803718322"} or renderer_path.stat().st_size != 13411 or _repository_text_sha256(renderer_path.read_bytes()) != renderer["sha256"]:
        errors.append("M6 reviewer renderer identity changed")
    public_manifest = record.get("public_manifest", {})
    if public_manifest.get("bytes") != manifest_path.stat().st_size or public_manifest.get("sha256") != _repository_text_sha256(manifest_path.read_bytes()) or public_manifest.get("artifacts") != 9:
        errors.append("M6 public evidence manifest identity changed")
    expected_renders = {
        "docs/evidence/generated/architecture.svg": (3414, "3c7de3ddb7b3ec5c7b0275bc151edfbb745686254920d86f9eab58e684562495"),
        "docs/evidence/generated/training-curves.svg": (18645, "d4b8e2578ba8a5de35ddf9435f6cd832b04fb07d3bfbe055f212d48b580478f7"),
        "docs/evidence/generated/comparative-summary.svg": (7121, "880e9ec02d6178510e69a5a723b278a11f859401e1ccdbd66f5ab278a8ae128c"),
    }
    observed_renders = {item.get("path"): (item.get("bytes"), item.get("sha256")) for item in record.get("rendered_surfaces", [])}
    if observed_renders != expected_renders:
        errors.append("M6 reviewer render roster changed")
    for relative, (size, digest) in expected_renders.items():
        path = root / relative
        if not path.is_file() or path.stat().st_size != size or _repository_text_sha256(path.read_bytes()) != digest:
            errors.append(f"M6 reviewer render bytes changed: {relative}")
    attempts = record.get("retained_attempts", [])
    if [(item.get("attempt_id"), item.get("disposition")) for item in attempts] != [("m6-u002-001", "fail")] or record.get("accepted_attempt", {}).get("attempt_id") != "m6-u002-002":
        errors.append("M6 reviewer visual attempt retention changed")
    boundary = record.get("boundary_verification", {})
    if boundary.get("svg_embedded_images") != 0 or boundary.get("repository_forbidden_binary_extensions") != 0 or boundary.get("forbidden_bytes_included") != 0:
        errors.append("M6 reviewer evidence byte boundary changed")
    if manifest.get("forbidden_bytes_included") != 0 or manifest.get("dispositions") != {"comparative_status": "FAIL", "lifecycle_status": "PASS"} or len(manifest.get("artifacts", [])) != 9:
        errors.append("M6 public evidence manifest content changed")
    return errors


def check_release_candidate_audit(root: Path) -> list[str]:
    """Bind the exact prepublication candidate, verified surfaces, and asset."""

    paths = (RELEASE_SURFACE_MATRIX, RELEASE_AUDIT, RELEASE_CANDIDATE, MILESTONE_SIX_CONTROL_PROFILE)
    if any(not (root / relative).is_file() for relative in paths):
        return []
    try:
        matrix, audit, candidate = (
            _load_json(root / relative)
            for relative in (RELEASE_SURFACE_MATRIX, RELEASE_AUDIT, RELEASE_CANDIDATE)
        )
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M6 release candidate records must be UTF-8 JSON"]
    errors: list[str] = []
    commit = "a123fd1ff1b48089890cb9eb6a2d81d043a717a9"
    tree = "0e582fa09db39a49309f660d5244ffaacdcb0912"
    archive_sha = "ac811cb42511a2ec5c1163a1a9f193dcf4bd3637485a452b526a06435511f8e4"
    required_surfaces = {
        "repository_control",
        "repository_tests",
        "scientific_replay",
        "reviewer_evidence",
        "release_package",
    }
    profile_sha = hashlib.sha256((root / MILESTONE_SIX_CONTROL_PROFILE).read_bytes()).hexdigest()
    if matrix.get("candidate_identity") != commit or matrix.get("registry_sha256") != profile_sha:
        errors.append("M6 release surface matrix candidate or profile binding changed")
    receipts = {
        item.get("surface_id"): item
        for item in matrix.get("receipts", [])
        if isinstance(item, dict)
    }
    if set(matrix.get("surface_ids", [])) != required_surfaces or set(receipts) != required_surfaces or any(
        item.get("status") != "pass" or item.get("candidate_identity") != commit
        for item in receipts.values()
    ):
        errors.append("M6 release surface receipts are incomplete or changed")
    audit_candidate = audit.get("candidate", {})
    audit_matrix = audit.get("real_surface_matrix", {})
    decision = audit.get("decision", {})
    if audit_candidate.get("commit") != commit or audit_candidate.get("tree") != tree or audit_candidate.get("version") != "1.0.0" or audit_candidate.get("tag") != "v1.0.0":
        errors.append("M6 audited candidate identity changed")
    if audit_matrix.get("status") != "verified" or audit_matrix.get("candidate_identity") != commit or set(audit_matrix.get("required_surface_ids", [])) != required_surfaces or set(audit_matrix.get("verified_surface_ids", [])) != required_surfaces:
        errors.append("M6 audited real-surface disposition changed")
    if decision.get("reported_status") != "verified" or "github_pull_request_management" not in decision.get("authorized_next_actions", []):
        errors.append("M6 candidate audit decision changed")
    asset = candidate.get("release_asset", {})
    dispositions = candidate.get("dispositions", {})
    verification = candidate.get("verification", {})
    if candidate.get("candidate_commit") != commit or candidate.get("candidate_tree") != tree or candidate.get("status") != "eligible_for_reviewed_main_publication":
        errors.append("M6 release candidate identity or eligibility changed")
    if asset.get("bytes") != 34007 or asset.get("sha256") != archive_sha or asset.get("checksum_sha256") != "f23c50e4da2a7669a77120843b6dbc9ea02442964725606e52da61af232097e3":
        errors.append("M6 release asset identity changed")
    if dispositions != {"lifecycle_status": "PASS", "comparative_status": "FAIL", "post_test_changes": 0}:
        errors.append("M6 release dispositions changed")
    if verification.get("scientific_replay_status") != "PASS" or verification.get("package_verifier_status") != "PASS" or verification.get("approved_runtime_tests") != 56 or verification.get("tracked_forbidden_binary_files") != 0 or verification.get("secret_pattern_matches") != 0:
        errors.append("M6 release verification summary changed")
    if candidate.get("publication_boundary", {}).get("full_scientific_replay_requires_controlled_custody") is not True:
        errors.append("M6 release custody boundary changed")
    return errors


def check_live_release_record(root: Path) -> list[str]:
    """Bind the one verified GitHub release and all seven live surfaces."""

    paths = (LIVE_RELEASE_RECORD, LIVE_RELEASE_SURFACE_MATRIX, LIVE_RELEASE_AUDIT, MILESTONE_SIX_RELEASE_PROFILE)
    if any(not (root / relative).is_file() for relative in paths):
        return []
    try:
        record, matrix, audit = (
            _load_json(root / relative)
            for relative in (LIVE_RELEASE_RECORD, LIVE_RELEASE_SURFACE_MATRIX, LIVE_RELEASE_AUDIT)
        )
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["M6 live release records must be UTF-8 JSON"]
    errors: list[str] = []
    commit = "8de60a3350a7c25942be8223bf9067c9460774d1"
    archive_sha = "ac811cb42511a2ec5c1163a1a9f193dcf4bd3637485a452b526a06435511f8e4"
    all_surfaces = {"repository_control", "repository_tests", "scientific_replay", "reviewer_evidence", "release_package", "github_public_repository", "github_release"}
    if record.get("status") != "PASS" or record.get("release", {}).get("id") != 376615584 or record.get("tag", {}).get("peeled_commit") != commit or record.get("tag", {}).get("exact") is not True:
        errors.append("M6 live release or tag identity changed")
    assets = {item.get("name"): item for item in record.get("assets", []) if isinstance(item, dict)}
    zip_asset = assets.get("burnlens-experiment-three-v1.0.0-evidence.zip", {})
    if len(assets) != 2 or zip_asset.get("bytes") != 34007 or zip_asset.get("downloaded_sha256") != archive_sha or any(item.get("download_verification") != "PASS" for item in assets.values()):
        errors.append("M6 live release asset verification changed")
    sources = record.get("source_archive_verification", {})
    if sources.get("zip_tar_and_tag_worktree_exact") is not True or sources.get("files_each") != 136 or sources.get("bytes_each") != 1511185 or sources.get("roster_sha256") != "60a2da69f2ad3532621628a3d29f225e0a63401b4ddc59c78ef31224657382ca":
        errors.append("M6 source archive verification changed")
    if record.get("public_byte_boundary") != {"forbidden_bytes_in_release": 0, "full_scientific_replay_requires_controlled_custody": True, "public_package_is_full_scientific_replay": False}:
        errors.append("M6 live release byte boundary changed")
    profile_sha = hashlib.sha256((root / MILESTONE_SIX_RELEASE_PROFILE).read_bytes()).hexdigest()
    receipts = {item.get("surface_id"): item for item in matrix.get("receipts", []) if isinstance(item, dict)}
    if matrix.get("candidate_identity") != commit or matrix.get("registry_sha256") != profile_sha or set(matrix.get("surface_ids", [])) != all_surfaces or set(receipts) != all_surfaces or any(item.get("status") != "pass" for item in receipts.values()):
        errors.append("M6 live real-surface matrix changed")
    audit_matrix = audit.get("real_surface_matrix", {})
    if audit.get("candidate", {}).get("commit") != commit or audit.get("decision", {}).get("reported_status") != "verified" or audit_matrix.get("status") != "verified" or set(audit_matrix.get("verified_surface_ids", [])) != all_surfaces:
        errors.append("M6 live release audit changed")
    return errors


def check_terminal_closeout_record(root: Path) -> list[str]:
    """Require one released terminal outcome and no successor work."""

    record_path = root / TERMINAL_CLOSEOUT_RECORD
    profile_path = root / CONTROL_PROFILE
    milestone_path = root / TERMINAL_RELEASE_MILESTONE
    if not record_path.is_file() or not profile_path.is_file() or not milestone_path.is_file():
        return []
    try:
        record = _load_json(record_path)
        profile = _load_json(profile_path)
        milestone = _load_json(milestone_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["terminal closeout records must be UTF-8 JSON"]
    errors: list[str] = []
    if record.get("status") != "PASS_ON_PR15_LIVE_ACCEPTANCE" or record.get("goal_id") != "01a03021-0d66-7553-bcab-26971ec191e6":
        errors.append("terminal closeout identity or transaction changed")
    if record.get("scientific_dispositions") != {"lifecycle_status": "PASS", "comparative_status": "FAIL", "post_test_changes": 0}:
        errors.append("terminal scientific dispositions changed")
    if record.get("scientific_outputs") != {"datasets": 1, "training_runs": 3, "checkpoints": 3, "inference_runs": 6, "evaluations": 1, "releases": 1}:
        errors.append("terminal scientific outputs changed")
    if record.get("completed_milestones") != [0, 1, 2, 3, 4, 5, 6] or record.get("no_active_or_successor_work") is not True or record.get("next_action_after_acceptance") is not None:
        errors.append("terminal completion or successor boundary changed")
    continuation = record.get("continuation_boundary", {})
    if any(value is not False for value in continuation.values()) or set(continuation) != {"experiment_three_b_authorized", "fresh_confirmation_authorized", "post_test_tuning_authorized", "new_release_authorized"}:
        errors.append("terminal continuation boundary changed")
    if profile.get("scientific_state") != "terminal_released_closed" or profile.get("scientific_outputs") != record.get("scientific_outputs"):
        errors.append("terminal profile state changed")
    units = {item.get("id"): item for item in milestone.get("units", []) if isinstance(item, dict)}
    exits = {item.get("id"): item.get("status") for item in milestone.get("exit_conditions", []) if isinstance(item, dict)}
    if milestone.get("status") != "complete" or units.get("M6-U006-TERMINAL-CLOSEOUT", {}).get("status") != "complete" or any(status != "pass" for status in exits.values()):
        errors.append("terminal milestone is not fully complete")
    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    checks = (
        check_required_files,
        check_checkout_portability,
        check_json_documents,
        check_no_cloud_sync_references,
        check_no_scientific_artifacts,
        check_control_references,
        check_truthful_bootstrap_state,
        check_milestone_one_identity_inventory,
        check_owner_rights_review_preparation,
        check_milestone_one_admission_chain,
        check_runtime_adoption_review_preparation,
        check_runtime_failure_and_successor_review,
        check_synthetic_preflight_record,
        check_frozen_protocol_record,
        check_frozen_training_record,
        check_preopening_audit,
        check_evaluation_path_preflight,
        check_retrospective_evaluation_record,
        check_reviewer_evidence_record,
        check_release_candidate_audit,
        check_live_release_record,
        check_terminal_closeout_record,
    )
    errors: list[str] = []
    for check in checks:
        errors.extend(check(root))
    return errors


def main() -> int:
    errors = validate_repository(ROOT)
    if errors:
        print(f"Repository controls: FAIL ({len(errors)} finding(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Repository controls: PASS "
        f"({len(REQUIRED_FILES)} required files; active milestone truth verified)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
