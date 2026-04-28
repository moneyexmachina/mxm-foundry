# tests/conftest.py

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def minimal_project(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# Example\n")
    (tmp_path / "LICENSE").write_text("MIT\n")
    (tmp_path / "pyproject.toml").write_text("[tool.poetry]\nname = 'mxm-example'\n")
    (tmp_path / "pyrightconfig.json").write_text("{}\n")
    (tmp_path / "Makefile").write_text("check:\n\t@echo check\n")

    return tmp_path
