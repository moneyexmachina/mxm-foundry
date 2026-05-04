# src/mxm/foundry/checks/policies/documentation.py

from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

DOCUMENTATION_POLICY = Policy(
    code="POLICY_DOCUMENTATION",
    name="Documentation policy",
    checks=(
        get_check("FS001"),
        get_check("FS010"),
        get_check("DOC001"),
        get_check("DOC002"),
    ),
)
