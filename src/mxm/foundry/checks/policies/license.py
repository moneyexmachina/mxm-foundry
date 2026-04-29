from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

LICENSE_POLICY = Policy(
    code="POLICY_LICENSE",
    name="License policy",
    checks=(
        get_check("FS002"),
        get_check("LIC001"),
    ),
)
