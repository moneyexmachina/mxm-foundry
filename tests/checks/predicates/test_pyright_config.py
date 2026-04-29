from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _pytest.monkeypatch import MonkeyPatch

from mxm.foundry.checks.predicates import pyright_config
from mxm.foundry.checks.predicates.golden import load_json_object
from mxm.foundry.checks.predicates.pyright_config import (
    PYRIGHT_CONFIG_CHECKS,
    check_pyright_config_matches_canonical,
)

JsonDoc = dict[str, Any]


def write_json(path: Path, data: JsonDoc) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def canonical_pyright_config() -> JsonDoc:
    policy_doc, error = load_json_object(pyright_config.POLICY_PYRIGHTCONFIG_PATH)

    assert policy_doc is not None, error

    return dict(policy_doc)


def test_pyright_config_check_passes_when_project_matches_canonical(
    tmp_path: Path,
) -> None:
    write_json(
        tmp_path / "pyrightconfig.json",
        canonical_pyright_config(),
    )

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "pass"
    assert result.code == "PY030"
    assert result.path == tmp_path / "pyrightconfig.json"
    assert result.message == "pyrightconfig.json matches canonical MXM config."


def test_pyright_config_check_fails_when_project_differs_from_canonical(
    tmp_path: Path,
) -> None:
    config = canonical_pyright_config()
    config["pythonVersion"] = "3.12"

    write_json(tmp_path / "pyrightconfig.json", config)

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == tmp_path / "pyrightconfig.json"
    assert result.message == "pyrightconfig.json does not match canonical MXM config."


def test_pyright_config_check_uses_policy_path(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    project_config = {"pythonVersion": "3.13"}
    alternate_policy_config = {"pythonVersion": "3.13"}

    policy_path = tmp_path / "policy" / "pyrightconfig.json"
    policy_path.parent.mkdir()

    write_json(tmp_path / "pyrightconfig.json", project_config)
    write_json(policy_path, alternate_policy_config)

    monkeypatch.setattr(
        pyright_config,
        "POLICY_PYRIGHTCONFIG_PATH",
        policy_path,
    )

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "pass"
    assert result.path == tmp_path / "pyrightconfig.json"


def test_pyright_config_check_fails_when_policy_path_is_missing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    write_json(tmp_path / "pyrightconfig.json", canonical_pyright_config())

    policy_path = tmp_path / "missing_policy" / "pyrightconfig.json"

    monkeypatch.setattr(
        pyright_config,
        "POLICY_PYRIGHTCONFIG_PATH",
        policy_path,
    )

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == policy_path
    assert "File not found" in result.message


def test_pyright_config_checks_tuple_contains_py030() -> None:
    assert len(PYRIGHT_CONFIG_CHECKS) == 1

    check = PYRIGHT_CONFIG_CHECKS[0]

    assert check.code == "PY030"
    assert check.name == "pyrightconfig.json matches canonical config"
