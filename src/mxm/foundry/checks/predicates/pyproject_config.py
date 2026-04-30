from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult
from mxm.foundry.checks.toml_utils import load_toml, nested_mapping

POLICY_PYPROJECT_PATH = Path(__file__).parents[2] / "canonical" / "pyproject.toml"


def check_config_block_matches_canonical(
    project_root: Path,
    code: str,
    block_path: tuple[str, ...],
    block_name: str,
) -> CheckResult:
    """Check that a pyproject.toml config block matches the canonical MXM config."""

    check_name = f"{block_name} matches canonical config"
    project_pyproject_path = project_root / "pyproject.toml"

    project_doc, project_error = load_toml(project_pyproject_path)
    if project_doc is None:
        return CheckResult(
            code=code,
            name=check_name,
            status="fail",
            message=project_error or "Cannot inspect project pyproject.toml.",
            path=project_pyproject_path,
        )

    policy_doc, policy_error = load_toml(POLICY_PYPROJECT_PATH)
    if policy_doc is None:
        return CheckResult(
            code=code,
            name=check_name,
            status="fail",
            message=policy_error or "Cannot inspect canonical pyproject policy.",
            path=POLICY_PYPROJECT_PATH,
        )

    project_config = nested_mapping(project_doc, block_path)
    if project_config is None:
        return CheckResult(
            code=code,
            name=check_name,
            status="fail",
            message=f"Project pyproject.toml is missing {block_name}.",
            path=project_pyproject_path,
        )

    policy_config = nested_mapping(policy_doc, block_path)
    if policy_config is None:
        return CheckResult(
            code=code,
            name=check_name,
            status="fail",
            message=f"Canonical policy pyproject.toml is missing {block_name}.",
            path=POLICY_PYPROJECT_PATH,
        )

    if dict(project_config) == dict(policy_config):
        return CheckResult(
            code=code,
            name=check_name,
            status="pass",
            message=f"{block_name} matches canonical MXM config.",
            path=project_pyproject_path,
        )

    return CheckResult(
        code=code,
        name=check_name,
        status="fail",
        message=f"{block_name} does not match canonical MXM config.",
        path=project_pyproject_path,
    )


def check_black_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.black] matches the canonical MXM configuration."""

    return check_config_block_matches_canonical(
        project_root=project_root,
        code=code,
        block_path=("tool", "black"),
        block_name="[tool.black]",
    )


def check_ruff_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.ruff] matches the canonical MXM configuration."""

    return check_config_block_matches_canonical(
        project_root=project_root,
        code=code,
        block_path=("tool", "ruff"),
        block_name="[tool.ruff]",
    )


def check_ruff_lint_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.ruff.lint] matches the canonical MXM configuration."""

    return check_config_block_matches_canonical(
        project_root=project_root,
        code=code,
        block_path=("tool", "ruff", "lint"),
        block_name="[tool.ruff.lint]",
    )


def check_ruff_lint_isort_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.ruff.lint.isort] matches the canonical MXM configuration."""

    return check_config_block_matches_canonical(
        project_root=project_root,
        code=code,
        block_path=("tool", "ruff", "lint", "isort"),
        block_name="[tool.ruff.lint.isort]",
    )


def check_isort_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that [tool.isort] matches the canonical MXM configuration."""

    return check_config_block_matches_canonical(
        project_root=project_root,
        code=code,
        block_path=("tool", "isort"),
        block_name="[tool.isort]",
    )


PYPROJECT_CONFIG_CHECKS: tuple[Check, ...] = (
    Check(
        code="PY020",
        name="[tool.black] matches canonical config",
        run=lambda root: check_black_config_matches_canonical(root, "PY020"),
    ),
    Check(
        code="PY021",
        name="[tool.ruff] matches canonical config",
        run=lambda root: check_ruff_config_matches_canonical(root, "PY021"),
    ),
    Check(
        code="PY022",
        name="[tool.ruff.lint] matches canonical config",
        run=lambda root: check_ruff_lint_config_matches_canonical(root, "PY022"),
    ),
    Check(
        code="PY023",
        name="[tool.ruff.lint.isort] matches canonical config",
        run=lambda root: check_ruff_lint_isort_config_matches_canonical(root, "PY023"),
    ),
    Check(
        code="PY024",
        name="[tool.isort] matches canonical config",
        run=lambda root: check_isort_config_matches_canonical(root, "PY024"),
    ),
)
