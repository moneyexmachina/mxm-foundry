from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

from mxm.foundry.checks.models import Check, CheckResult
from mxm.foundry.checks.toml_utils import (
    TomlMapping,
    load_toml,
    nested_mapping,
)


def _load_pyproject(project_root: Path) -> tuple[TomlMapping | None, str | None]:
    return load_toml(project_root / "pyproject.toml")


def _tool_poetry(document: TomlMapping) -> TomlMapping | None:
    return nested_mapping(document, ("tool", "poetry"))


def check_pyproject_parseable(project_root: Path, code: str) -> CheckResult:
    path = project_root / "pyproject.toml"

    document, error = _load_pyproject(project_root)

    if document is not None:
        return CheckResult(
            code=code,
            name="pyproject.toml is parseable",
            status="pass",
            message="pyproject.toml is valid TOML.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="pyproject.toml is parseable",
        status="fail",
        message=error or "pyproject.toml could not be parsed.",
        path=path,
    )


def check_tool_poetry_exists(project_root: Path, code: str) -> CheckResult:
    path = project_root / "pyproject.toml"

    document, error = _load_pyproject(project_root)
    if document is None:
        return CheckResult(
            code=code,
            name="[tool.poetry] exists",
            status="fail",
            message=error or "Cannot inspect [tool.poetry].",
            path=path,
        )

    poetry = _tool_poetry(document)
    if poetry is not None:
        return CheckResult(
            code=code,
            name="[tool.poetry] exists",
            status="pass",
            message="Found [tool.poetry].",
            path=path,
        )

    return CheckResult(
        code=code,
        name="[tool.poetry] exists",
        status="fail",
        message="Missing [tool.poetry] section.",
        path=path,
    )


def check_poetry_name_starts_with_mxm(project_root: Path, code: str) -> CheckResult:
    path = project_root / "pyproject.toml"

    document, error = _load_pyproject(project_root)
    if document is None:
        return CheckResult(
            code=code,
            name="Poetry project name starts with mxm-",
            status="fail",
            message=error or "Cannot inspect Poetry project name.",
            path=path,
        )

    poetry = _tool_poetry(document)
    if poetry is None:
        return CheckResult(
            code=code,
            name="Poetry project name starts with mxm-",
            status="fail",
            message="Cannot inspect Poetry project name because [tool.poetry] is missing.",
            path=path,
        )

    name = poetry.get("name")
    if not isinstance(name, str):
        return CheckResult(
            code=code,
            name="Poetry project name starts with mxm-",
            status="fail",
            message="Poetry project name is missing or not a string.",
            path=path,
        )

    if name.startswith("mxm-"):
        return CheckResult(
            code=code,
            name="Poetry project name starts with mxm-",
            status="pass",
            message=f"Poetry project name is {name!r}.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="Poetry project name starts with mxm-",
        status="fail",
        message=f"Poetry project name must start with 'mxm-'; found {name!r}.",
        path=path,
    )


def check_poetry_package_uses_src_mxm_layout(
    project_root: Path, code: str
) -> CheckResult:
    path = project_root / "pyproject.toml"

    document, error = _load_pyproject(project_root)
    if document is None:
        return CheckResult(
            code=code,
            name="Poetry package uses src/mxm layout",
            status="fail",
            message=error or "Cannot inspect Poetry package layout.",
            path=path,
        )

    poetry = _tool_poetry(document)
    if poetry is None:
        return CheckResult(
            code=code,
            name="Poetry package uses src/mxm layout",
            status="fail",
            message="Cannot inspect Poetry package layout because [tool.poetry] is missing.",
            path=path,
        )

    name = poetry.get("name")
    if not isinstance(name, str):
        return CheckResult(
            code=code,
            name="Poetry package uses src/mxm layout",
            status="fail",
            message="Cannot infer package layout because Poetry project name is missing or not a string.",
            path=path,
        )

    if not name.startswith("mxm-"):
        return CheckResult(
            code=code,
            name="Poetry package uses src/mxm layout",
            status="fail",
            message=f"Cannot infer MXM import name because project name does not start with 'mxm-': {name!r}.",
            path=path,
        )

    import_name = name.removeprefix("mxm-").replace("-", "_")
    expected_include = f"mxm/{import_name}"
    packages_value = poetry.get("packages")
    if not isinstance(packages_value, Sequence) or isinstance(packages_value, str):
        return CheckResult(
            code=code,
            name="Poetry package uses src/mxm layout",
            status="fail",
            message="tool.poetry.packages is missing or not a list.",
            path=path,
        )
    packages = cast(Sequence[Any], packages_value)
    for package_value in packages:
        if not isinstance(package_value, Mapping):
            continue

        package = cast(Mapping[str, Any], package_value)

        if package.get("include") == expected_include and package.get("from") == "src":
            return CheckResult(
                code=code,
                name="Poetry package uses src/mxm layout",
                status="pass",
                message=f"Found package include {expected_include!r} from 'src'.",
                path=path,
            )
    return CheckResult(
        code=code,
        name="Poetry package uses src/mxm layout",
        status="fail",
        message=f"Expected tool.poetry.packages to include {{ include = {expected_include!r}, from = 'src' }}.",
        path=path,
    )


def check_tool_pyright_absent(project_root: Path, code: str) -> CheckResult:
    path = project_root / "pyproject.toml"

    document, error = _load_pyproject(project_root)
    if document is None:
        return CheckResult(
            code=code,
            name="[tool.pyright] is absent",
            status="fail",
            message=error or "Cannot inspect [tool.pyright].",
            path=path,
        )

    pyright = nested_mapping(document, ("tool", "pyright"))

    if pyright is None:
        return CheckResult(
            code=code,
            name="[tool.pyright] is absent",
            status="pass",
            message="No [tool.pyright] section found.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="[tool.pyright] is absent",
        status="fail",
        message="[tool.pyright] must not be defined; use pyrightconfig.json instead.",
        path=path,
    )


PYPROJECT_CHECKS: tuple[Check, ...] = (
    Check(
        code="PY001",
        name="pyproject.toml is parseable",
        run=lambda root: check_pyproject_parseable(root, "PY001"),
    ),
    Check(
        code="PY002",
        name="[tool.poetry] exists",
        run=lambda root: check_tool_poetry_exists(root, "PY002"),
    ),
    Check(
        code="PY003",
        name="Poetry project name starts with mxm-",
        run=lambda root: check_poetry_name_starts_with_mxm(root, "PY003"),
    ),
    Check(
        code="PY004",
        name="Poetry package uses src/mxm layout",
        run=lambda root: check_poetry_package_uses_src_mxm_layout(root, "PY004"),
    ),
    Check(
        code="PY031",
        name="[tool.pyright] is absent",
        run=lambda root: check_tool_pyright_absent(root, "PY031"),
    ),
)
