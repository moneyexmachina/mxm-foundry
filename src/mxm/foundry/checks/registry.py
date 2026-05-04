from __future__ import annotations

from mxm.foundry.checks.models import Check, Policy
from mxm.foundry.checks.predicates.documentation import DOCUMENTATION_CHECKS
from mxm.foundry.checks.predicates.filesystem import FILESYSTEM_CHECKS
from mxm.foundry.checks.predicates.license import LICENSE_CHECKS
from mxm.foundry.checks.predicates.makefile import MAKEFILE_CHECKS
from mxm.foundry.checks.predicates.pyproject import PYPROJECT_CHECKS
from mxm.foundry.checks.predicates.pyproject_config import PYPROJECT_CONFIG_CHECKS
from mxm.foundry.checks.predicates.pyright_config import PYRIGHT_CONFIG_CHECKS

CHECKS: tuple[Check, ...] = (
    *FILESYSTEM_CHECKS,
    *LICENSE_CHECKS,
    *PYPROJECT_CHECKS,
    *PYPROJECT_CONFIG_CHECKS,
    *PYRIGHT_CONFIG_CHECKS,
    *MAKEFILE_CHECKS,
    *DOCUMENTATION_CHECKS,
)

_CHECK_BY_CODE: dict[str, Check] = {}

for check in CHECKS:
    if check.code in _CHECK_BY_CODE:
        raise ValueError(f"Duplicate check code detected: {check.code}")
    _CHECK_BY_CODE[check.code] = check


def get_check(code: str) -> Check:
    """Retrieve a Check by its code."""

    try:
        return _CHECK_BY_CODE[code]
    except KeyError as exc:
        raise KeyError(f"Check with code '{code}' not found.") from exc


from mxm.foundry.checks.policies.check_gate import CHECK_GATE_POLICY  # noqa: E402
from mxm.foundry.checks.policies.documentation import DOCUMENTATION_POLICY  # noqa: E402
from mxm.foundry.checks.policies.formatting import FORMATTING_POLICY  # noqa: E402

# Import policies only after CHECKS and get_check are fully defined.
from mxm.foundry.checks.policies.license import LICENSE_POLICY  # noqa: E402
from mxm.foundry.checks.policies.pyproject import PYPROJECT_POLICY  # noqa: E402
from mxm.foundry.checks.policies.testing import TESTING_POLICY  # noqa: E402
from mxm.foundry.checks.policies.typing import TYPING_POLICY  # noqa: E402

POLICIES: tuple[Policy, ...] = (
    LICENSE_POLICY,
    TYPING_POLICY,
    FORMATTING_POLICY,
    PYPROJECT_POLICY,
    TESTING_POLICY,
    CHECK_GATE_POLICY,
    DOCUMENTATION_POLICY,
)


def policy_check_codes() -> set[str]:
    """Return all check codes used by at least one registered policy."""

    return {check.code for policy in POLICIES for check in policy.checks}


def misc_checks() -> tuple[Check, ...]:
    """Return checks not currently covered by any registered policy."""

    covered_codes = policy_check_codes()

    return tuple(check for check in CHECKS if check.code not in covered_codes)
