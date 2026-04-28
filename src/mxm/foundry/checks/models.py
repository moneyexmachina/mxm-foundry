from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CheckStatus = Literal["pass", "warn", "fail"]


@dataclass(frozen=True)
class CheckResult:
    """Structured result of evaluating one MXM package predicate."""

    code: str
    name: str
    status: CheckStatus
    message: str
    path: Path | None = None
