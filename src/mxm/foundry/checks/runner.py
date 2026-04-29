from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import (
    CheckResult,
    Policy,
    PolicyResult,
    aggregate_check_status,
)
from mxm.foundry.checks.registry import CHECKS, POLICIES, misc_checks


def run_policy(policy: Policy, project_root: Path) -> PolicyResult:
    """Run all checks in one flat policy against a project root."""

    root = project_root.resolve()
    results = tuple(check.run(root) for check in policy.checks)

    return PolicyResult(
        code=policy.code,
        name=policy.name,
        status=aggregate_check_status(results),
        checks=results,
    )


def run_checks(project_root: Path) -> list[CheckResult]:
    """Run MXM package checks against a project root."""

    root = project_root.resolve()

    return [check.run(root) for check in CHECKS]


def run_policies(project_root: Path) -> list[PolicyResult]:
    """Run MXM policies against a project root."""

    root = project_root.resolve()

    return [run_policy(policy, root) for policy in POLICIES]


def run_misc_checks(project_root: Path) -> list[CheckResult]:
    """Run checks not covered by any registered policy."""

    root = project_root.resolve()

    return [check.run(root) for check in misc_checks()]
