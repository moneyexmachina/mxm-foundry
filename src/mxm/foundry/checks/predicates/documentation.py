from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult

REQUIRED_README_SECTIONS = [
    "## Purpose",
    "## Installation",
    "## Usage",
    "## Development",
]


def check_readme_has_required_sections(
    project_root: Path,
    code: str,
) -> CheckResult:
    path = project_root / "README.md"

    try:
        contents = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return CheckResult(
            code=code,
            name="README.md has required sections",
            status="fail",
            message="README.md is missing.",
            path=path,
        )

    missing = [
        section for section in REQUIRED_README_SECTIONS if section not in contents
    ]

    if not missing:
        return CheckResult(
            code=code,
            name="README.md has required sections",
            status="pass",
            message="README.md contains all required sections.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="README.md has required sections",
        status="fail",
        message=f"Missing sections: {', '.join(missing)}.",
        path=path,
    )


def check_changelog_has_minimal_structure(
    project_root: Path,
    code: str,
) -> CheckResult:
    path = project_root / "CHANGELOG.md"

    try:
        contents = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return CheckResult(
            code=code,
            name="CHANGELOG.md has minimal structure",
            status="fail",
            message="CHANGELOG.md is missing.",
            path=path,
        )

    required = ["# Changelog", "## Unreleased"]

    missing = [section for section in required if section not in contents]

    if not missing:
        return CheckResult(
            code=code,
            name="CHANGELOG.md has minimal structure",
            status="pass",
            message="CHANGELOG.md has minimal required structure.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="CHANGELOG.md has minimal structure",
        status="fail",
        message=f"Missing sections: {', '.join(missing)}.",
        path=path,
    )


DOCUMENTATION_CHECKS: tuple[Check, ...] = (
    Check(
        code="DOC001",
        name="README.md has required sections",
        run=lambda root: check_readme_has_required_sections(root, "DOC001"),
    ),
    Check(
        code="DOC002",
        name="CHANGELOG.md has minimal structure",
        run=lambda root: check_changelog_has_minimal_structure(root, "DOC002"),
    ),
)
