from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult


def check_required_file(
    project_root: Path, relative_path: str, code: str
) -> CheckResult:
    """Check that a required file exists at the project root."""

    path = project_root / relative_path

    if path.is_file():
        return CheckResult(
            code=code,
            name=f"{relative_path} exists",
            status="pass",
            message=f"Found {relative_path}.",
            path=path,
        )

    return CheckResult(
        code=code,
        name=f"{relative_path} exists",
        status="fail",
        message=f"Missing required file: {relative_path}.",
        path=path,
    )


def check_required_directory(
    project_root: Path,
    relative_path: str,
    code: str,
) -> CheckResult:
    """Check that a required directory exists at the project root."""

    path = project_root / relative_path

    if path.is_dir():
        return CheckResult(
            code=code,
            name=f"{relative_path} directory exists",
            status="pass",
            message=f"Found directory: {relative_path}.",
            path=path,
        )

    return CheckResult(
        code=code,
        name=f"{relative_path} directory exists",
        status="fail",
        message=f"Missing required directory: {relative_path}.",
        path=path,
    )


def check_single_mxm_package(project_root: Path, code: str) -> CheckResult:
    """Check that exactly one package directory exists under src/mxm."""

    mxm_root = project_root / "src" / "mxm"

    if not mxm_root.is_dir():
        return CheckResult(
            code=code,
            name="single MXM package directory exists",
            status="fail",
            message="Cannot inspect package directory because src/mxm is missing.",
            path=mxm_root,
        )

    package_dirs = sorted(
        path
        for path in mxm_root.iterdir()
        if path.is_dir() and path.name != "__pycache__"
    )

    if len(package_dirs) == 1:
        return CheckResult(
            code=code,
            name="single MXM package directory exists",
            status="pass",
            message=f"Found package directory: src/mxm/{package_dirs[0].name}.",
            path=package_dirs[0],
        )

    if not package_dirs:
        return CheckResult(
            code=code,
            name="single MXM package directory exists",
            status="fail",
            message="No package directory found under src/mxm.",
            path=mxm_root,
        )

    names = ", ".join(path.name for path in package_dirs)
    return CheckResult(
        code=code,
        name="single MXM package directory exists",
        status="fail",
        message=f"Expected exactly one package under src/mxm; found {len(package_dirs)}: {names}.",
        path=mxm_root,
    )


def check_package_py_typed(project_root: Path, code: str) -> CheckResult:
    """Check that the discovered MXM package contains a py.typed marker."""

    mxm_root = project_root / "src" / "mxm"

    if not mxm_root.is_dir():
        return CheckResult(
            code=code,
            name="package py.typed exists",
            status="fail",
            message="Cannot inspect py.typed because src/mxm is missing.",
            path=mxm_root,
        )

    package_dirs = sorted(
        path
        for path in mxm_root.iterdir()
        if path.is_dir() and path.name != "__pycache__"
    )

    if len(package_dirs) != 1:
        return CheckResult(
            code=code,
            name="package py.typed exists",
            status="fail",
            message="Cannot inspect py.typed because exactly one package directory was not found.",
            path=mxm_root,
        )

    py_typed_path = package_dirs[0] / "py.typed"

    if py_typed_path.is_file():
        return CheckResult(
            code=code,
            name="package py.typed exists",
            status="pass",
            message=f"Found py.typed in src/mxm/{package_dirs[0].name}.",
            path=py_typed_path,
        )

    return CheckResult(
        code=code,
        name="package py.typed exists",
        status="fail",
        message=f"Missing py.typed in src/mxm/{package_dirs[0].name}.",
        path=py_typed_path,
    )


def check_changelog_exists(project_root: Path, code: str) -> CheckResult:
    path = project_root / "CHANGELOG.md"

    if path.exists():
        return CheckResult(
            code=code,
            name="CHANGELOG.md exists",
            status="pass",
            message="Found CHANGELOG.md.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="CHANGELOG.md exists",
        status="fail",
        message="CHANGELOG.md is missing.",
        path=path,
    )


FILESYSTEM_CHECKS: tuple[Check, ...] = (
    Check(
        code="FS001",
        name="README.md exists",
        run=lambda root: check_required_file(root, "README.md", "FS001"),
    ),
    Check(
        code="FS002",
        name="LICENSE exists",
        run=lambda root: check_required_file(root, "LICENSE", "FS002"),
    ),
    Check(
        code="FS003",
        name="pyproject.toml exists",
        run=lambda root: check_required_file(root, "pyproject.toml", "FS003"),
    ),
    Check(
        code="FS004",
        name="pyrightconfig.json exists",
        run=lambda root: check_required_file(root, "pyrightconfig.json", "FS004"),
    ),
    Check(
        code="FS005",
        name="Makefile exists",
        run=lambda root: check_required_file(root, "Makefile", "FS005"),
    ),
    Check(
        code="FS006",
        name="tests directory exists",
        run=lambda root: check_required_directory(root, "tests", "FS006"),
    ),
    Check(
        code="FS007",
        name="src/mxm directory exists",
        run=lambda root: check_required_directory(root, "src/mxm", "FS007"),
    ),
    Check(
        code="FS008",
        name="single MXM package directory exists",
        run=lambda root: check_single_mxm_package(root, "FS008"),
    ),
    Check(
        code="FS009",
        name="package py.typed exists",
        run=lambda root: check_package_py_typed(root, "FS009"),
    ),
    Check(
        code="FS010",
        name="CHANGELOG.md exists",
        run=lambda root: check_changelog_exists(root, "FS010"),
    ),
)
