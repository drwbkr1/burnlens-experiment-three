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
CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-005.json"
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

REQUIRED_FILES = (
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
    Path("docs/devlog/2026-08-23-empty-bootstrap.md"),
    Path("docs/devlog/2026-08-24-milestone-one-intake.md"),
    Path("docs/devlog/2026-08-24-milestone-two-runtime-gate.md"),
    Path("records/decisions/DECISION-REGISTER.md"),
    Path("records/evidence/EVIDENCE-LEDGER.md"),
    Path("records/governance/EXPERIMENT-THREE-AUTHORITY-2026-001.md"),
    HISTORICAL_CONTROL_PROFILE,
    MILESTONE_ONE_CONTROL_PROFILE,
    MILESTONE_TWO_CONTROL_PROFILE,
    MILESTONE_THREE_CONTROL_PROFILE,
    CONTROL_PROFILE,
    BOOTSTRAP_MILESTONE,
    PROVENANCE_MILESTONE,
    SYNTHETIC_PREFLIGHT_MILESTONE,
    PROTOCOL_FREEZE_MILESTONE,
    FROZEN_TRAINING_MILESTONE,
    STATE_RECONCILIATION,
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-002.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-003.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-004.json"),
    Path("records/reconciliations/EXPERIMENT-THREE-STATE-2026-005.json"),
    Path("records/training/README.md"),
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
    Path("docs/devlog/2026-08-24-milestone-three-protocol-freeze.md"),
    Path("scripts/validate_frozen_protocol.py"),
    Path("scripts/run_protocol_dry_run.py"),
    Path("scripts/validate_repository.py"),
    Path("tests/test_repository_controls.py"),
    Path("tests/test_frozen_protocol.py"),
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


def validate_repository(root: Path = ROOT) -> list[str]:
    checks = (
        check_required_files,
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
