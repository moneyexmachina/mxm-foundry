from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mxm.foundry.checks.predicates.golden import (
    check_json_file_matches_golden,
    check_text_file_matches_golden,
    load_json_object,
    load_text,
)

JsonDoc = dict[str, Any]


def write_json(path: Path, data: JsonDoc) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_load_text_loads_utf8_text_file(tmp_path: Path) -> None:
    path = tmp_path / "example.txt"
    path.write_text("hello\n", encoding="utf-8")

    text, error = load_text(path)

    assert text == "hello\n"
    assert error is None


def test_load_text_fails_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.txt"

    text, error = load_text(path)

    assert text is None
    assert error is not None
    assert "File not found" in error


def test_load_json_object_loads_object_document(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    write_json(path, {"key": "value"})

    document, error = load_json_object(path)

    assert document == {"key": "value"}
    assert error is None


def test_load_json_object_fails_when_file_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    document, error = load_json_object(path)

    assert document is None
    assert error is not None
    assert "File not found" in error


def test_load_json_object_fails_when_json_is_invalid(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{invalid-json", encoding="utf-8")

    document, error = load_json_object(path)

    assert document is None
    assert error is not None
    assert "Invalid JSON" in error


def test_load_json_object_fails_when_top_level_value_is_not_object(
    tmp_path: Path,
) -> None:
    path = tmp_path / "list.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    document, error = load_json_object(path)

    assert document is None
    assert error is not None
    assert "Expected top-level JSON object" in error


def test_check_text_file_matches_golden_passes_when_text_is_identical(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "LICENSE"
    golden_path.parent.mkdir()

    (project_root / "LICENSE").write_text("canonical license\n", encoding="utf-8")
    golden_path.write_text("canonical license\n", encoding="utf-8")

    result = check_text_file_matches_golden(
        project_root=project_root,
        relative_path=Path("LICENSE"),
        golden_path=golden_path,
        code="FS003",
        name="LICENSE matches canonical license",
        pass_message="LICENSE matches canonical MXM license.",
        fail_message="LICENSE does not match canonical MXM license.",
    )

    assert result.status == "pass"
    assert result.code == "FS003"
    assert result.path == project_root / "LICENSE"
    assert result.message == "LICENSE matches canonical MXM license."


def test_check_text_file_matches_golden_fails_when_project_file_is_missing(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "LICENSE"
    golden_path.parent.mkdir()
    golden_path.write_text("canonical license\n", encoding="utf-8")

    result = check_text_file_matches_golden(
        project_root=project_root,
        relative_path=Path("LICENSE"),
        golden_path=golden_path,
        code="FS003",
        name="LICENSE matches canonical license",
        pass_message="LICENSE matches canonical MXM license.",
        fail_message="LICENSE does not match canonical MXM license.",
    )

    assert result.status == "fail"
    assert result.code == "FS003"
    assert result.path == project_root / "LICENSE"
    assert "File not found" in result.message


def test_check_text_file_matches_golden_fails_when_golden_file_is_missing(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "LICENSE").write_text("canonical license\n", encoding="utf-8")

    golden_path = tmp_path / "policy" / "LICENSE"

    result = check_text_file_matches_golden(
        project_root=project_root,
        relative_path=Path("LICENSE"),
        golden_path=golden_path,
        code="FS003",
        name="LICENSE matches canonical license",
        pass_message="LICENSE matches canonical MXM license.",
        fail_message="LICENSE does not match canonical MXM license.",
    )

    assert result.status == "fail"
    assert result.code == "FS003"
    assert result.path == golden_path
    assert "File not found" in result.message


def test_check_text_file_matches_golden_fails_when_text_differs(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "LICENSE"
    golden_path.parent.mkdir()

    (project_root / "LICENSE").write_text("modified license\n", encoding="utf-8")
    golden_path.write_text("canonical license\n", encoding="utf-8")

    result = check_text_file_matches_golden(
        project_root=project_root,
        relative_path=Path("LICENSE"),
        golden_path=golden_path,
        code="FS003",
        name="LICENSE matches canonical license",
        pass_message="LICENSE matches canonical MXM license.",
        fail_message="LICENSE does not match canonical MXM license.",
    )

    assert result.status == "fail"
    assert result.code == "FS003"
    assert result.path == project_root / "LICENSE"
    assert result.message == "LICENSE does not match canonical MXM license."


def test_check_json_file_matches_golden_passes_when_objects_are_equal(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "pyrightconfig.json"
    golden_path.parent.mkdir()

    write_json(project_root / "pyrightconfig.json", {"pythonVersion": "3.13"})
    write_json(golden_path, {"pythonVersion": "3.13"})

    result = check_json_file_matches_golden(
        project_root=project_root,
        relative_path=Path("pyrightconfig.json"),
        golden_path=golden_path,
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        pass_message="pyrightconfig.json matches canonical MXM config.",
        fail_message="pyrightconfig.json does not match canonical MXM config.",
    )

    assert result.status == "pass"
    assert result.code == "PY030"
    assert result.path == project_root / "pyrightconfig.json"
    assert result.message == "pyrightconfig.json matches canonical MXM config."


def test_check_json_file_matches_golden_fails_when_project_json_is_invalid(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "pyrightconfig.json"
    golden_path.parent.mkdir()

    (project_root / "pyrightconfig.json").write_text("{invalid-json", encoding="utf-8")
    write_json(golden_path, {"pythonVersion": "3.13"})

    result = check_json_file_matches_golden(
        project_root=project_root,
        relative_path=Path("pyrightconfig.json"),
        golden_path=golden_path,
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        pass_message="pyrightconfig.json matches canonical MXM config.",
        fail_message="pyrightconfig.json does not match canonical MXM config.",
    )

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == project_root / "pyrightconfig.json"
    assert "Invalid JSON" in result.message


def test_check_json_file_matches_golden_fails_when_golden_json_is_invalid(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "pyrightconfig.json"
    golden_path.parent.mkdir()

    write_json(project_root / "pyrightconfig.json", {"pythonVersion": "3.13"})
    golden_path.write_text("{invalid-json", encoding="utf-8")

    result = check_json_file_matches_golden(
        project_root=project_root,
        relative_path=Path("pyrightconfig.json"),
        golden_path=golden_path,
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        pass_message="pyrightconfig.json matches canonical MXM config.",
        fail_message="pyrightconfig.json does not match canonical MXM config.",
    )

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == golden_path
    assert "Invalid JSON" in result.message


def test_check_json_file_matches_golden_fails_when_objects_differ(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    golden_path = tmp_path / "policy" / "pyrightconfig.json"
    golden_path.parent.mkdir()

    write_json(project_root / "pyrightconfig.json", {"pythonVersion": "3.12"})
    write_json(golden_path, {"pythonVersion": "3.13"})

    result = check_json_file_matches_golden(
        project_root=project_root,
        relative_path=Path("pyrightconfig.json"),
        golden_path=golden_path,
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        pass_message="pyrightconfig.json matches canonical MXM config.",
        fail_message="pyrightconfig.json does not match canonical MXM config.",
    )

    assert result.status == "fail"
    assert result.code == "PY030"
    assert result.path == project_root / "pyrightconfig.json"
    assert result.message == "pyrightconfig.json does not match canonical MXM config."
