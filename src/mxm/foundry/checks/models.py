from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CheckStatus = Literal["pass", "warn", "fail"]


@dataclass(frozen=True)
class Check:
    """Executable MXM package check.

    A Check binds a stable predicate code and display name to a function that
    evaluates one project-root-level predicate.
    """

    code: str
    name: str
    run: Callable[[Path], CheckResult]


@dataclass(frozen=True)
class CheckResult:
    """Structured result of evaluating one MXM package predicate."""

    code: str
    name: str
    status: CheckStatus
    message: str
    path: Path | None = None


@dataclass(frozen=True)
class Policy:
    """Named composition of atomic checks.

    A Policy groups related checks into a higher-level assertion about one
    coherent aspect of a project, such as licensing, Pyright configuration, or
    package metadata.

    Policies are intentionally flat in v0.1: they contain checks, not nested
    policies.
    """

    code: str
    name: str
    checks: tuple[Check, ...]


@dataclass(frozen=True)
class PolicyResult:
    """Result of evaluating a Policy against a project."""

    code: str
    name: str
    status: Literal["pass", "fail"]
    checks: tuple[CheckResult, ...]


def aggregate_check_status(
    results: Sequence[CheckResult],
) -> Literal["pass", "fail"]:
    """Aggregate atomic check results into a policy-level status."""

    return "pass" if all(result.status == "pass" for result in results) else "fail"
