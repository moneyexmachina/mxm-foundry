from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult
from mxm.foundry.checks.predicates.golden import check_text_file_matches_golden

POLICY_LICENSE_PATH = Path(__file__).parents[2] / "canonical" / "LICENSE"


def check_license_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that LICENSE matches the canonical MXM license file."""

    return check_text_file_matches_golden(
        project_root=project_root,
        relative_path=Path("LICENSE"),
        golden_path=POLICY_LICENSE_PATH,
        code=code,
        name="LICENSE matches canonical license",
        pass_message="LICENSE matches canonical MXM license.",
        fail_message="LICENSE does not match canonical MXM license.",
    )


LICENSE_CHECKS: tuple[Check, ...] = (
    Check(
        code="LIC001",
        name="LICENSE matches canonical license",
        run=lambda root: check_license_matches_canonical(root, "LIC001"),
    ),
)
