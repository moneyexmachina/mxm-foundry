from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult
from mxm.foundry.checks.toml_utils import load_toml, nested_mapping

POLICY_PYPROJECT_PATH = Path(__file__).parents[2] / "canonical" / "pyproject.toml"


def check_black_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.black] matches the canonical MXM configuration."""

    project_pyproject_path = project_root / "pyproject.toml"

    project_doc, project_error = load_toml(project_pyproject_path)
    if project_doc is None:
        return CheckResult(
            code=code,
            name="[tool.black] matches canonical config",
            status="fail",
            message=project_error or "Cannot inspect project pyproject.toml.",
            path=project_pyproject_path,
        )

    policy_doc, policy_error = load_toml(POLICY_PYPROJECT_PATH)
    if policy_doc is None:
        return CheckResult(
            code=code,
            name="[tool.black] matches canonical config",
            status="fail",
            message=policy_error or "Cannot inspect canonical pyproject policy.",
            path=POLICY_PYPROJECT_PATH,
        )

    project_black = nested_mapping(project_doc, ("tool", "black"))
    if project_black is None:
        return CheckResult(
            code=code,
            name="[tool.black] matches canonical config",
            status="fail",
            message="Project pyproject.toml is missing [tool.black].",
            path=project_pyproject_path,
        )

    policy_black = nested_mapping(policy_doc, ("tool", "black"))
    if policy_black is None:
        return CheckResult(
            code=code,
            name="[tool.black] matches canonical config",
            status="fail",
            message="Canonical policy pyproject.toml is missing [tool.black].",
            path=POLICY_PYPROJECT_PATH,
        )

    if dict(project_black) == dict(policy_black):
        return CheckResult(
            code=code,
            name="[tool.black] matches canonical config",
            status="pass",
            message="[tool.black] matches canonical MXM config.",
            path=project_pyproject_path,
        )

    return CheckResult(
        code=code,
        name="[tool.black] matches canonical config",
        status="fail",
        message="[tool.black] does not match canonical MXM config.",
        path=project_pyproject_path,
    )


PYPROJECT_CONFIG_CHECKS: tuple[Check, ...] = (
    Check(
        code="PY020",
        name="[tool.black] matches canonical config",
        run=lambda root: check_black_config_matches_canonical(root, "PY020"),
    ),
)
