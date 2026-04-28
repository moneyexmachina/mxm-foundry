from __future__ import annotations

from pathlib import Path

import tomlkit

from mxm.foundry.checks.toml_utils import (
    load_toml,
    mapping_value,
    nested_mapping,
)


def test_load_toml_pass(tmp_path: Path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.poetry]\nname = 'mxm-example'\n")

    document, error = load_toml(path)

    assert document is not None
    assert error is None
    assert document["tool"]["poetry"]["name"] == "mxm-example"


def test_load_toml_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "pyproject.toml"

    document, error = load_toml(path)

    assert document is None
    assert error is not None
    assert "missing" in error.lower()


def test_load_toml_invalid(tmp_path: Path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.poetry\nname = 'mxm-example'\n")

    document, error = load_toml(path)

    assert document is None
    assert error is not None
    assert "not valid" in error.lower()


def test_mapping_value_pass(tmp_path: Path) -> None:
    _ = tmp_path
    doc = tomlkit.parse(
        """
[tool.poetry]
name = "mxm-example"
"""
    )

    tool = mapping_value(doc, "tool")

    assert tool is not None
    assert isinstance(tool, dict)


def test_mapping_value_returns_none_for_non_mapping(tmp_path: Path) -> None:
    _ = tmp_path
    doc = {"tool": "not-a-dict"}

    result = mapping_value(doc, "tool")

    assert result is None


def test_nested_mapping_pass(tmp_path: Path) -> None:
    _ = tmp_path
    doc = tomlkit.parse(
        """
[tool.poetry]
name = "mxm-example"
"""
    )

    poetry = nested_mapping(doc, ("tool", "poetry"))

    assert poetry is not None
    assert poetry["name"] == "mxm-example"


def test_nested_mapping_missing_path(tmp_path: Path) -> None:
    _ = tmp_path
    doc = tomlkit.parse(
        """
[tool.black]
line-length = 88
"""
    )

    poetry = nested_mapping(doc, ("tool", "poetry"))

    assert poetry is None


def test_nested_mapping_stops_on_non_mapping(tmp_path: Path) -> None:
    _ = tmp_path
    doc = {"tool": "not-a-dict"}

    result = nested_mapping(doc, ("tool", "poetry"))

    assert result is None
