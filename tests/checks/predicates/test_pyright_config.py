from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _pytest.monkeypatch import MonkeyPatch

from mxm.foundry.checks.predicates import pyright_config
from mxm.foundry.checks.predicates.pyright_config import (
    check_pyright_config_matches_canonical,
    load_json,
)

JsonDoc = dict[str, Any]


def write_json(path: Path, data: JsonDoc) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def canonical_pyright_config() -> JsonDoc:
    policy_doc, error = load_json(pyright_config.POLICY_PYRIGHTCONFIG_PATH)

    assert policy_doc is not None, error

    return dict(policy_doc)


def test_load_json_loads_object_document(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    write_json(path, {"key": "value"})

    document, error = load_json(path)

    assert document == {"key": "value"}
    assert error is None


def test_load_json_fails_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    document, error = load_json(path)

    assert document is None
    assert error is not None
    assert "File not found" in error


def test_load_json_fails_when_json_is_invalid(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{invalid-json", encoding="utf-8")

    document, error = load_json(path)

    assert document is None
    assert error is not None
    assert "Invalid JSON" in error


def test_load_json_fails_when_top_level_value_is_not_object(tmp_path: Path) -> None:
    path = tmp_path / "list.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    document, error = load_json(path)

    assert document is None
    assert error is not None
    assert "Expected top-level JSON object" in error


def test_check_pyright_config_passes_when_project_matches_canonical(
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


def test_check_pyright_config_fails_when_project_file_is_missing(
    tmp_path: Path,
) -> None:
    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == tmp_path / "pyrightconfig.json"
    assert "File not found" in result.message


def test_check_pyright_config_fails_when_project_json_is_invalid(
    tmp_path: Path,
) -> None:
    path = tmp_path / "pyrightconfig.json"
    path.write_text("{invalid-json", encoding="utf-8")

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == path
    assert "Invalid JSON" in result.message


def test_check_pyright_config_fails_when_project_json_is_not_object(
    tmp_path: Path,
) -> None:
    path = tmp_path / "pyrightconfig.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    result = check_pyright_config_matches_canonical(tmp_path, "PY030")

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == path
    assert "Expected top-level JSON object" in result.message


def test_check_pyright_config_fails_when_canonical_policy_file_is_missing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    policy_path = tmp_path / "missing_policy" / "pyrightconfig.json"

    write_json(
        tmp_path / "pyrightconfig.json",
        canonical_pyright_config(),
    )

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


def test_check_pyright_config_fails_when_project_differs_from_canonical(
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
