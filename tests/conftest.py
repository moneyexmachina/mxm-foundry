from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from mxm.foundry.checks.predicates import pyproject_config, pyright_config


@pytest.fixture
def minimal_valid_project(tmp_path: Path) -> Path:
    """Create a minimal MXM project satisfying current canonical checks."""

    project_root = tmp_path / "minimal-project"

    package_root = project_root / "src" / "mxm" / "example"
    tests_root = project_root / "tests"

    package_root.mkdir(parents=True)
    tests_root.mkdir(parents=True)

    shutil.copyfile(
        pyproject_config.POLICY_PYPROJECT_PATH,
        project_root / "pyproject.toml",
    )
    shutil.copyfile(
        pyright_config.POLICY_PYRIGHTCONFIG_PATH,
        project_root / "pyrightconfig.json",
    )

    (project_root / "README.md").write_text(
        "# mxm-example\n",
        encoding="utf-8",
    )

    (package_root / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package_root / "py.typed").write_text(
        "",
        encoding="utf-8",
    )
    (project_root / "LICENSE").write_text(
        "MIT License\n",
        encoding="utf-8",
    )

    (project_root / "Makefile").write_text(
        ".PHONY: test check\n\n"
        "test:\n"
        "\tpoetry run pytest\n\n"
        "check:\n"
        "\tpoetry run ruff check .\n",
        encoding="utf-8",
    )
    return project_root
