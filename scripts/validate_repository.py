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
CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-002.json"
)
BOOTSTRAP_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-000-BOOTSTRAP-2026-001.json"
)
PROVENANCE_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-001-PROVENANCE-2026-001.json"
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
    Path("records/decisions/DECISION-REGISTER.md"),
    Path("records/evidence/EVIDENCE-LEDGER.md"),
    Path("records/governance/EXPERIMENT-THREE-AUTHORITY-2026-001.md"),
    HISTORICAL_CONTROL_PROFILE,
    CONTROL_PROFILE,
    BOOTSTRAP_MILESTONE,
    PROVENANCE_MILESTONE,
    STATE_RECONCILIATION,
    Path("records/prompt-build-log/2026-08-23-bootstrap.md"),
    Path("scripts/validate_repository.py"),
    Path("tests/test_repository_controls.py"),
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
        "no_go",
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
    policy_label = "bootstrap" if policy == "bootstrap" else "milestone 1"
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

    active_relative, error = _checked_relative_path(
        profile.get("active_milestone_path"), "active_milestone_path"
    )
    if error or active_relative is None:
        return errors

    state = profile.get("scientific_state")
    if not isinstance(state, str) or state.casefold() != "not_started":
        policy_label = "bootstrap" if policy == "bootstrap" else "milestone 1"
        errors.append(f"{policy_label} scientific_state must be 'not_started'")

    profile_outputs = profile.get("scientific_outputs")
    if policy == "milestone_1" and not isinstance(profile_outputs, dict):
        errors.append("milestone 1 profile scientific_outputs must be a JSON object")

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
        policy_label = "bootstrap" if policy == "bootstrap" else "milestone 1"
        return errors + [
            f"{policy_label} milestone scientific_outputs must be a JSON object"
        ]
    policy_label = "bootstrap" if policy == "bootstrap" else "milestone 1"
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

    if policy == "milestone_1" and isinstance(profile_outputs, dict):
        for field in MILESTONE_ONE_ZERO_OUTPUT_FIELDS:
            value = profile_outputs.get(field)
            if type(value) is not int or value != 0:
                errors.append(
                    "milestone 1 profile "
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
                    f"milestone 1 {location} scientific_outputs.datasets "
                    "must be integer 0 or 1"
                )
        if (
            type(profile_datasets) is int
            and type(milestone_datasets) is int
            and profile_datasets != milestone_datasets
        ):
            errors.append(
                "milestone 1 profile and milestone "
                "scientific_outputs.datasets must match"
            )

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


def validate_repository(root: Path = ROOT) -> list[str]:
    checks = (
        check_required_files,
        check_json_documents,
        check_no_cloud_sync_references,
        check_no_scientific_artifacts,
        check_control_references,
        check_truthful_bootstrap_state,
        check_milestone_one_identity_inventory,
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
