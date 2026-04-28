from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import CheckResult
from mxm.foundry.checks.predicates import check_required_file


def run_checks(project_root: Path) -> list[CheckResult]:
    """Run MXM package checks against a project root."""

    root = project_root.resolve()

    return [
        check_required_file(root, "README.md", "FS001"),
        check_required_file(root, "LICENSE", "FS002"),
        check_required_file(root, "pyproject.toml", "FS003"),
        check_required_file(root, "pyrightconfig.json", "FS004"),
        check_required_file(root, "Makefile", "FS005"),
    ]
