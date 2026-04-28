# tests/conftest.py

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def minimal_valid_project(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# Example\n")
    (tmp_path / "LICENSE").write_text("MIT\n")
    (tmp_path / "pyproject.toml").write_text("[tool.poetry]\nname = 'mxm-example'\n")
    (tmp_path / "pyrightconfig.json").write_text("{}\n")
    (tmp_path / "Makefile").write_text("check:\n\t@echo check\n")

    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text(
        """
[tool.poetry]
name = "mxm-example"
packages = [{ include = "mxm/example", from = "src" }]
"""
    )
    package_root = tmp_path / "src" / "mxm" / "example"
    package_root.mkdir(parents=True)
    (package_root / "__init__.py").write_text("")
    (package_root / "py.typed").write_text("")

    return tmp_path
