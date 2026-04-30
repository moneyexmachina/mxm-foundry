# src/mxm/foundry/checks/policies/formatting.py

from __future__ import annotations

from mxm.foundry.checks.models import Policy
from mxm.foundry.checks.registry import get_check

FORMATTING_POLICY = Policy(
    code="POLICY_FORMATTING",
    name="Formatting policy",
    checks=(
        get_check("PY020"),  # [tool.black]
        get_check("PY021"),  # [tool.ruff]
        get_check("PY022"),  # [tool.ruff.lint]
        get_check("PY023"),  # [tool.ruff.lint.isort]
        get_check("PY024"),  # [tool.isort]
        get_check("MK003"),  # lint target exists
        get_check("MK004"),  # lint target commands match canonical
        get_check("MK005"),  # fmt target exists
        get_check("MK006"),  # fmt target commands match canonical
    ),
)
