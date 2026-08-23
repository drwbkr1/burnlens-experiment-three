#!/usr/bin/env python3
"""Validate the repository control plane without third-party dependencies."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]

CONTROL_PROFILE = Path(
    "records/governance/"
    "EXPERIMENT-THREE-PROJECT-CONTROL-PROFILE-2026-001.json"
)
BOOTSTRAP_MILESTONE = Path(
    "records/milestones/"
    "EXPERIMENT-THREE-MILESTONE-000-BOOTSTRAP-2026-001.json"
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
    CONTROL_PROFILE,
    BOOTSTRAP_MILESTONE,
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
    "models",
    "outputs",
    "runs",
}

EMPTY_OUTPUT_FIELDS = (
    "datasets",
    "training_runs",
    "checkpoints",
    "inference_runs",
    "evaluations",
    "releases",
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


def check_no_scientific_artifacts(root: Path) -> list[str]:
    profile_path = root / CONTROL_PROFILE
    if profile_path.is_file():
        try:
            profile = _load_json(profile_path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            profile = None
        if isinstance(profile, dict):
            active = profile.get("active_milestone_path")
            if isinstance(active, str) and "BOOTSTRAP" not in Path(active).name.upper():
                return []

    errors: list[str] = []
    for path in _repository_files(root):
        relative = path.relative_to(root)
        suffix = path.suffix.casefold()
        if suffix in PROHIBITED_ARTIFACT_SUFFIXES:
            errors.append(f"prohibited bootstrap artifact type: {relative.as_posix()}")
            continue
        directory_parts = {part.casefold() for part in relative.parts[:-1]}
        forbidden_parts = directory_parts & PROHIBITED_ARTIFACT_DIRECTORIES
        if forbidden_parts:
            errors.append(f"prohibited bootstrap artifact location: {relative.as_posix()}")
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
    """Require explicit zero scientific outputs while bootstrap is active."""

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

    active_relative, error = _checked_relative_path(
        profile.get("active_milestone_path"), "active_milestone_path"
    )
    if error or active_relative is None:
        return errors
    if "BOOTSTRAP" not in active_relative.name.upper():
        return errors

    state = profile.get("scientific_state")
    if not isinstance(state, str) or state.casefold() != "not_started":
        errors.append("bootstrap scientific_state must be 'not_started'")

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
        return errors + ["bootstrap scientific_outputs must be a JSON object"]
    for field in EMPTY_OUTPUT_FIELDS:
        value = outputs.get(field)
        if type(value) is not int or value != 0:
            errors.append(f"bootstrap scientific_outputs.{field} must be integer 0")
    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    checks = (
        check_required_files,
        check_json_documents,
        check_no_cloud_sync_references,
        check_no_scientific_artifacts,
        check_control_references,
        check_truthful_bootstrap_state,
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
        f"({len(REQUIRED_FILES)} required files; bootstrap truth verified)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
