from __future__ import annotations

from collections.abc import Callable
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
