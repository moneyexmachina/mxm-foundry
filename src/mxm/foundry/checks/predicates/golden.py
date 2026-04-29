from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from mxm.foundry.checks.models import CheckResult


def load_text(path: Path) -> tuple[str | None, str | None]:
    """Load a UTF-8 text file from disk."""

    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load a JSON file whose top-level value must be an object."""

    try:
        with path.open("rb") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {path}: {exc}"
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"

    if not isinstance(raw, dict):
        return None, f"Expected top-level JSON object in {path}."

    return cast(dict[str, Any], raw), None


def check_text_file_matches_golden(
    *,
    project_root: Path,
    relative_path: Path,
    golden_path: Path,
    code: str,
    name: str,
    pass_message: str,
    fail_message: str,
) -> CheckResult:
    """Check that a project text file exactly matches a canonical text file."""

    project_path = project_root / relative_path

    project_text, project_error = load_text(project_path)
    if project_text is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=project_error or f"Cannot inspect project file: {project_path}",
            path=project_path,
        )

    golden_text, golden_error = load_text(golden_path)
    if golden_text is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=golden_error or f"Cannot inspect golden file: {golden_path}",
            path=golden_path,
        )

    if project_text == golden_text:
        return CheckResult(
            code=code,
            name=name,
            status="pass",
            message=pass_message,
            path=project_path,
        )

    return CheckResult(
        code=code,
        name=name,
        status="fail",
        message=fail_message,
        path=project_path,
    )


def check_json_file_matches_golden(
    *,
    project_root: Path,
    relative_path: Path,
    golden_path: Path,
    code: str,
    name: str,
    pass_message: str,
    fail_message: str,
) -> CheckResult:
    """Check that a project JSON object semantically matches a canonical JSON object."""

    project_path = project_root / relative_path

    project_doc, project_error = load_json_object(project_path)
    if project_doc is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=project_error
            or f"Cannot inspect project JSON file: {project_path}",
            path=project_path,
        )

    golden_doc, golden_error = load_json_object(golden_path)
    if golden_doc is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=golden_error or f"Cannot inspect golden JSON file: {golden_path}",
            path=golden_path,
        )

    if project_doc == golden_doc:
        return CheckResult(
            code=code,
            name=name,
            status="pass",
            message=pass_message,
            path=project_path,
        )

    return CheckResult(
        code=code,
        name=name,
        status="fail",
        message=fail_message,
        path=project_path,
    )
