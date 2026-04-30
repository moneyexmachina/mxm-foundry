from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

PYRIGHT_POLICY = Policy(
    code="POLICY_PYRIGHT",
    name="Pyright policy",
    checks=(
        get_check("FS004"),
        get_check("PY030"),
        get_check("PY031"),
        get_check("MK001"),
        get_check("MK002"),
    ),
)
