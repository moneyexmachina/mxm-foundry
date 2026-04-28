from __future__ import annotations

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates.filesystem import (
    FILESYSTEM_CHECKS,
)

CHECKS: tuple[Check, ...] = (*FILESYSTEM_CHECKS,)
