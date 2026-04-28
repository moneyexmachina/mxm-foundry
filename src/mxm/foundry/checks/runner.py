from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import CheckResult
from mxm.foundry.checks.registry import CHECKS


def run_checks(project_root: Path) -> list[CheckResult]:
    """Run MXM package checks against a project root."""

    root = project_root.resolve()

    return [check.run(root) for check in CHECKS]
