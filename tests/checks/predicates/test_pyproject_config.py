from __future__ import annotations

from pathlib import Path
from typing import Any

import tomli_w
from _pytest.monkeypatch import MonkeyPatch

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates import pyproject_config
from mxm.foundry.checks.predicates.pyproject_config import (
    check_black_config_matches_canonical,
)
from mxm.foundry.checks.toml_utils import load_toml, nested_mapping

TomlDoc = dict[str, Any]


def write_pyproject(project_root: Path, content: str) -> Path:
    path = project_root / "pyproject.toml"
    path.write_text(content, encoding="utf-8")
    return path


def write_toml(path: Path, data: TomlDoc) -> None:
    path.write_text(tomli_w.dumps(data), encoding="utf-8")


def canonical_black_config() -> dict[str, Any]:
    policy_doc, error = load_toml(pyproject_config.POLICY_PYPROJECT_PATH)

    assert policy_doc is not None, error

    black_config = nested_mapping(policy_doc, ("tool", "black"))

    assert black_config is not None

    return dict(black_config)


def test_check_black_config_passes_when_project_matches_canonical(
    tmp_path: Path,
) -> None:
    write_toml(
        tmp_path / "pyproject.toml",
        {"tool": {"black": canonical_black_config()}},
    )

    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "pass"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"


def test_check_black_config_fails_when_project_pyproject_is_missing(
    tmp_path: Path,
) -> None:
    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert "pyproject.toml" in result.message


def test_check_black_config_fails_when_project_pyproject_is_invalid(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.black\n")

    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert "pyproject.toml" in result.message


def test_check_black_config_fails_when_project_is_missing_black_block(
    tmp_path: Path,
) -> None:
    write_toml(tmp_path / "pyproject.toml", {"tool": {"ruff": {}}})

    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == "Project pyproject.toml is missing [tool.black]."


def test_check_black_config_fails_when_canonical_policy_is_missing_black_block(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    policy_root = tmp_path / "policy"
    project_root.mkdir()
    policy_root.mkdir()

    project_pyproject = project_root / "pyproject.toml"
    policy_pyproject = policy_root / "pyproject.toml"

    write_toml(project_pyproject, {"tool": {"black": {"line-length": 88}}})
    write_toml(policy_pyproject, {"tool": {"ruff": {}}})

    monkeypatch.setattr(
        pyproject_config,
        "POLICY_PYPROJECT_PATH",
        policy_pyproject,
    )

    result = check_black_config_matches_canonical(project_root, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == policy_pyproject
    assert result.message == "Canonical policy pyproject.toml is missing [tool.black]."


def test_check_black_config_fails_when_project_differs_from_canonical(
    tmp_path: Path,
) -> None:
    different_black_config = canonical_black_config()
    different_black_config["line-length"] = 1

    write_toml(
        tmp_path / "pyproject.toml",
        {"tool": {"black": different_black_config}},
    )

    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == "[tool.black] does not match canonical MXM config."


def test_pyproject_config_checks_include_black_canonical_check() -> None:
    checks_by_code: dict[str, Check] = {
        check.code: check for check in pyproject_config.PYPROJECT_CONFIG_CHECKS
    }

    assert "PY020" in checks_by_code
    assert checks_by_code["PY020"].name == "[tool.black] matches canonical config"
