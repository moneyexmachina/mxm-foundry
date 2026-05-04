from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from mxm.foundry.checks.predicates import makefile, pyproject_config, pyright_config
from mxm.foundry.checks.predicates.license import POLICY_LICENSE_PATH


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
    shutil.copyfile(
        POLICY_LICENSE_PATH,
        project_root / "LICENSE",
    )
    (project_root / "README.md").write_text(
        "# Example\n\n## Purpose\n\n## Installation\n\n## Usage\n\n## Development\n",
        encoding="utf-8",
    )

    (project_root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## Unreleased\n",
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
    shutil.copyfile(
        makefile.POLICY_MAKEFILE_PATH,
        project_root / "Makefile",
    )

    return project_root
