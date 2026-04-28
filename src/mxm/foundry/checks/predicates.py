from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import CheckResult


def check_required_file(
    project_root: Path, relative_path: str, code: str
) -> CheckResult:
    """Check that a required file exists at the project root."""

    path = project_root / relative_path

    if path.is_file():
        return CheckResult(
            code=code,
            name=f"{relative_path} exists",
            status="pass",
            message=f"Found {relative_path}.",
            path=path,
        )

    return CheckResult(
        code=code,
        name=f"{relative_path} exists",
        status="fail",
        message=f"Missing required file: {relative_path}.",
        path=path,
    )
