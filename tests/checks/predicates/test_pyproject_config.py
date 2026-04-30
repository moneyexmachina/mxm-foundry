from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import tomli_w
from _pytest.monkeypatch import MonkeyPatch

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates import pyproject_config
from mxm.foundry.checks.predicates.pyproject_config import (
    check_black_config_matches_canonical,
    check_config_block_matches_canonical,
    check_isort_config_matches_canonical,
    check_ruff_config_matches_canonical,
    check_ruff_lint_config_matches_canonical,
    check_ruff_lint_isort_config_matches_canonical,
)
from mxm.foundry.checks.toml_utils import load_toml, nested_mapping

TomlDoc = dict[str, Any]


CONFIG_CASES = [
    (
        "PY020",
        "[tool.black]",
        ("tool", "black"),
        check_black_config_matches_canonical,
    ),
    (
        "PY021",
        "[tool.ruff]",
        ("tool", "ruff"),
        check_ruff_config_matches_canonical,
    ),
    (
        "PY022",
        "[tool.ruff.lint]",
        ("tool", "ruff", "lint"),
        check_ruff_lint_config_matches_canonical,
    ),
    (
        "PY023",
        "[tool.ruff.lint.isort]",
        ("tool", "ruff", "lint", "isort"),
        check_ruff_lint_isort_config_matches_canonical,
    ),
    (
        "PY024",
        "[tool.isort]",
        ("tool", "isort"),
        check_isort_config_matches_canonical,
    ),
]


def write_pyproject(project_root: Path, content: str) -> Path:
    path = project_root / "pyproject.toml"
    path.write_text(content, encoding="utf-8")
    return path


def write_toml(path: Path, data: TomlDoc) -> None:
    path.write_text(tomli_w.dumps(data), encoding="utf-8")


def nested_dict(path: tuple[str, ...], value: Any) -> dict[str, Any]:
    result: Any = value
    for key in reversed(path):
        result = {key: result}
    return result


def canonical_config(block_path: tuple[str, ...]) -> dict[str, Any]:
    policy_doc, error = load_toml(pyproject_config.POLICY_PYPROJECT_PATH)

    assert policy_doc is not None, error

    config = nested_mapping(policy_doc, block_path)

    assert config is not None

    return dict(config)


@pytest.mark.parametrize(
    ("code", "block_name", "block_path", "check_func"),
    CONFIG_CASES,
)
def test_config_block_passes_when_project_matches_canonical(
    tmp_path: Path,
    code: str,
    block_name: str,
    block_path: tuple[str, ...],
    check_func: Any,
) -> None:
    write_toml(
        tmp_path / "pyproject.toml",
        nested_dict(block_path, canonical_config(block_path)),
    )

    result = check_func(tmp_path, code)

    assert result.status == "pass"
    assert result.code == code
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == f"{block_name} matches canonical MXM config."


def test_config_block_fails_when_project_pyproject_is_missing(
    tmp_path: Path,
) -> None:
    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert "pyproject.toml" in result.message


def test_config_block_fails_when_project_pyproject_is_invalid(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.black\n")

    result = check_black_config_matches_canonical(tmp_path, "PY020")

    assert result.status == "fail"
    assert result.code == "PY020"
    assert result.path == tmp_path / "pyproject.toml"
    assert "pyproject.toml" in result.message


@pytest.mark.parametrize(
    ("code", "block_name", "block_path", "check_func"),
    CONFIG_CASES,
)
def test_config_block_fails_when_project_is_missing_block(
    tmp_path: Path,
    code: str,
    block_name: str,
    block_path: tuple[str, ...],
    check_func: Any,
) -> None:
    write_toml(tmp_path / "pyproject.toml", {"tool": {"unrelated": {}}})

    result = check_func(tmp_path, code)

    assert result.status == "fail"
    assert result.code == code
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == f"Project pyproject.toml is missing {block_name}."


@pytest.mark.parametrize(
    ("code", "block_name", "block_path", "check_func"),
    CONFIG_CASES,
)
def test_config_block_fails_when_canonical_policy_is_missing_block(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    code: str,
    block_name: str,
    block_path: tuple[str, ...],
    check_func: Any,
) -> None:
    project_root = tmp_path / "project"
    policy_root = tmp_path / "policy"
    project_root.mkdir()
    policy_root.mkdir()

    project_pyproject = project_root / "pyproject.toml"
    policy_pyproject = policy_root / "pyproject.toml"

    write_toml(project_pyproject, nested_dict(block_path, {"line-length": 88}))
    write_toml(policy_pyproject, {"tool": {"unrelated": {}}})

    monkeypatch.setattr(
        pyproject_config,
        "POLICY_PYPROJECT_PATH",
        policy_pyproject,
    )

    result = check_func(project_root, code)

    assert result.status == "fail"
    assert result.code == code
    assert result.path == policy_pyproject
    assert result.message == f"Canonical policy pyproject.toml is missing {block_name}."


@pytest.mark.parametrize(
    ("code", "block_name", "block_path", "check_func"),
    CONFIG_CASES,
)
def test_config_block_fails_when_project_differs_from_canonical(
    tmp_path: Path,
    code: str,
    block_name: str,
    block_path: tuple[str, ...],
    check_func: Any,
) -> None:
    different_config = canonical_config(block_path)
    different_config["__mxm_test_difference__"] = True

    write_toml(
        tmp_path / "pyproject.toml",
        nested_dict(block_path, different_config),
    )

    result = check_func(tmp_path, code)

    assert result.status == "fail"
    assert result.code == code
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == f"{block_name} does not match canonical MXM config."


def test_check_config_block_matches_canonical_supports_arbitrary_nested_blocks(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    policy_root = tmp_path / "policy"
    project_root.mkdir()
    policy_root.mkdir()

    project_pyproject = project_root / "pyproject.toml"
    policy_pyproject = policy_root / "pyproject.toml"

    data = {"tool": {"example": {"nested": {"enabled": True}}}}

    write_toml(project_pyproject, data)
    write_toml(policy_pyproject, data)

    monkeypatch.setattr(
        pyproject_config,
        "POLICY_PYPROJECT_PATH",
        policy_pyproject,
    )

    result = check_config_block_matches_canonical(
        project_root=project_root,
        code="PY999",
        block_path=("tool", "example", "nested"),
        block_name="[tool.example.nested]",
    )

    assert result.status == "pass"
    assert result.code == "PY999"
    assert result.message == "[tool.example.nested] matches canonical MXM config."


def test_pyproject_config_checks_include_canonical_config_checks() -> None:
    checks_by_code: dict[str, Check] = {
        check.code: check for check in pyproject_config.PYPROJECT_CONFIG_CHECKS
    }

    expected = {
        "PY020": "[tool.black] matches canonical config",
        "PY021": "[tool.ruff] matches canonical config",
        "PY022": "[tool.ruff.lint] matches canonical config",
        "PY023": "[tool.ruff.lint.isort] matches canonical config",
        "PY024": "[tool.isort] matches canonical config",
    }

    assert set(expected).issubset(checks_by_code)

    for code, name in expected.items():
        assert checks_by_code[code].name == name
