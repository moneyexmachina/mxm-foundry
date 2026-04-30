# src/mxm/foundry/checks/policies/pyproject.py

from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

PYPROJECT_POLICY = Policy(
    code="POLICY_PYPROJECT",
    name="Pyproject policy",
    checks=(
        get_check("FS003"),
        get_check("PY001"),
        get_check("PY002"),
        get_check("PY003"),
        get_check("PY004"),
        get_check("PY005"),
        get_check("PY006"),
        get_check("PY007"),
        get_check("PY008"),
    ),
)
