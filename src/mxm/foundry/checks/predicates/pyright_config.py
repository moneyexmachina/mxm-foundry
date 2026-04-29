from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult
from mxm.foundry.checks.predicates.golden import check_json_file_matches_golden

POLICY_PYRIGHTCONFIG_PATH = (
    Path(__file__).parents[2] / "canonical" / "pyrightconfig.json"
)


def check_pyright_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that pyrightconfig.json matches the canonical MXM configuration."""

    return check_json_file_matches_golden(
        project_root=project_root,
        relative_path=Path("pyrightconfig.json"),
        golden_path=POLICY_PYRIGHTCONFIG_PATH,
        code=code,
        name="pyrightconfig.json matches canonical config",
        pass_message="pyrightconfig.json matches canonical MXM config.",
        fail_message="pyrightconfig.json does not match canonical MXM config.",
    )


PYRIGHT_CONFIG_CHECKS: tuple[Check, ...] = (
    Check(
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        run=lambda root: check_pyright_config_matches_canonical(root, "PY030"),
    ),
)
