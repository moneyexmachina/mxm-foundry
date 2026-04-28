from __future__ import annotations

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates.filesystem import (
    FILESYSTEM_CHECKS,
)
from mxm.foundry.checks.predicates.pyproject import PYPROJECT_CHECKS

CHECKS: tuple[Check, ...] = (
    *FILESYSTEM_CHECKS,
    *PYPROJECT_CHECKS,
)
