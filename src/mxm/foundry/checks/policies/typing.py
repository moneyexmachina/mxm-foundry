from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

TYPING_POLICY = Policy(
    code="POLICY_TYPING",
    name="Typing policy",
    checks=(
        # Filesystem typing marker
        get_check("FS009"),  # py.typed exists
        # Pyright config
        get_check("FS004"),
        get_check("PY030"),
        get_check("PY031"),
        # Makefile typing execution
        get_check("MK001"),
        get_check("MK002"),
        # Packaging typing guarantee
        get_check("PY009"),  # include py.typed
    ),
)
