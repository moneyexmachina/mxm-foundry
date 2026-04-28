from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from mxm.foundry.checks.models import Check, CheckResult

POLICY_PYRIGHTCONFIG_PATH = (
    Path(__file__).parents[2] / "policies" / "pyrightconfig.json"
)


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load a JSON object from disk."""

    try:
        with path.open("rb") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {path}: {exc}"
    except OSError as exc:
        return None, f"Cannot read {path}: {exc}"

    if not isinstance(raw, dict):
        return None, f"Expected top-level JSON object in {path}."

    document = cast(dict[str, Any], raw)

    return document, None


def check_pyright_config_matches_canonical(
    project_root: Path,
    code: str,
) -> CheckResult:
    """Check that pyrightconfig.json matches the canonical MXM configuration."""

    project_pyrightconfig_path = project_root / "pyrightconfig.json"

    project_doc, project_error = load_json(project_pyrightconfig_path)
    if project_doc is None:
        return CheckResult(
            code=code,
            name="pyrightconfig.json matches canonical config",
            status="fail",
            message=project_error or "Cannot inspect project pyrightconfig.json.",
            path=project_pyrightconfig_path,
        )

    policy_doc, policy_error = load_json(POLICY_PYRIGHTCONFIG_PATH)
    if policy_doc is None:
        return CheckResult(
            code=code,
            name="pyrightconfig.json matches canonical config",
            status="fail",
            message=policy_error or "Cannot inspect canonical pyrightconfig policy.",
            path=POLICY_PYRIGHTCONFIG_PATH,
        )

    if project_doc == policy_doc:
        return CheckResult(
            code=code,
            name="pyrightconfig.json matches canonical config",
            status="pass",
            message="pyrightconfig.json matches canonical MXM config.",
            path=project_pyrightconfig_path,
        )

    return CheckResult(
        code=code,
        name="pyrightconfig.json matches canonical config",
        status="fail",
        message="pyrightconfig.json does not match canonical MXM config.",
        path=project_pyrightconfig_path,
    )


PYRIGHT_CONFIG_CHECKS: tuple[Check, ...] = (
    Check(
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        run=lambda root: check_pyright_config_matches_canonical(root, "PY030"),
    ),
)
