# src/mxm/foundry/checks/policies/check_gate.py

from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

CHECK_GATE_POLICY = Policy(
    code="POLICY_CHECK_GATE",
    name="Check gate policy",
    checks=(
        get_check("FS005"),
        get_check("MK009"),
        get_check("MK010"),
        get_check("MK011"),
        get_check("MK012"),
    ),
)
