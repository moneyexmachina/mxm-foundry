# src/mxm/foundry/checks/policies/testing.py

from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

TESTING_POLICY = Policy(
    code="POLICY_TESTING",
    name="Testing policy",
    checks=(
        get_check("FS006"),
        get_check("MK007"),
        get_check("MK008"),
    ),
)
