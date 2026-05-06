from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.predicates.pyproject import (
    check_build_system_exists,
    check_mxm_package_matches_poetry_distribution_name,
    check_poetry_dependencies_exists,
    check_poetry_dev_dependencies_exists,
    check_poetry_include_contains_package_py_typed,
    check_poetry_name_starts_with_mxm,
    check_poetry_package_uses_src_mxm_layout,
    check_pyproject_parseable,
    check_pyproject_section_exists,
    check_pytest_ini_options_exists,
    check_tool_poetry_exists,
    check_tool_pyright_absent,
)


def write_pyproject(root: Path, content: str) -> None:
    (root / "pyproject.toml").write_text(content)


def test_check_pyproject_parseable_pass(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 'mxm-example'\n")

    result = check_pyproject_parseable(tmp_path, "PY001")

    assert result.status == "pass"
    assert result.code == "PY001"
    assert result.path == tmp_path / "pyproject.toml"


def test_check_pyproject_parseable_fails_when_missing(tmp_path: Path) -> None:
    result = check_pyproject_parseable(tmp_path, "PY001")

    assert result.status == "fail"
    assert result.code == "PY001"
    assert result.path == tmp_path / "pyproject.toml"


def test_check_pyproject_parseable_fails_when_invalid_toml(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.poetry\nname = 'mxm-example'\n")

    result = check_pyproject_parseable(tmp_path, "PY001")

    assert result.status == "fail"
    assert result.code == "PY001"


def test_check_tool_poetry_exists_pass(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 'mxm-example'\n")

    result = check_tool_poetry_exists(tmp_path, "PY002")

    assert result.status == "pass"
    assert result.code == "PY002"


def test_check_tool_poetry_exists_fails_when_missing(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.black]\nline-length = 88\n")

    result = check_tool_poetry_exists(tmp_path, "PY002")

    assert result.status == "fail"
    assert result.code == "PY002"


def test_check_tool_poetry_exists_fails_when_toml_invalid(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.poetry\nname = 'mxm-example'\n")

    result = check_tool_poetry_exists(tmp_path, "PY002")

    assert result.status == "fail"
    assert result.code == "PY002"


def test_check_poetry_name_starts_with_mxm_pass(tmp_path: Path) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 'mxm-example'\n")

    result = check_poetry_name_starts_with_mxm(tmp_path, "PY003")

    assert result.status == "pass"
    assert result.code == "PY003"


def test_check_poetry_name_starts_with_mxm_fails_when_name_has_wrong_prefix(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 'example'\n")

    result = check_poetry_name_starts_with_mxm(tmp_path, "PY003")

    assert result.status == "fail"
    assert result.code == "PY003"


def test_check_poetry_name_starts_with_mxm_fails_when_name_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\ndescription = 'Example'\n")

    result = check_poetry_name_starts_with_mxm(tmp_path, "PY003")

    assert result.status == "fail"
    assert result.code == "PY003"


def test_check_poetry_name_starts_with_mxm_fails_when_name_not_string(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 123\n")

    result = check_poetry_name_starts_with_mxm(tmp_path, "PY003")

    assert result.status == "fail"
    assert result.code == "PY003"


def test_check_poetry_package_uses_src_mxm_layout_pass(tmp_path: Path) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
packages = [{ include = "mxm", from = "src" }]
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "pass"
    assert result.code == "PY004"


def test_check_poetry_package_uses_src_mxm_layout_fails_when_packages_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "fail"
    assert result.code == "PY004"


def test_check_poetry_package_uses_src_mxm_layout_fails_when_include_wrong(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
packages = [{ include = "mxm/example", from = "src" }]
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "fail"
    assert result.code == "PY004"


def test_check_poetry_package_uses_src_mxm_layout_fails_when_from_wrong(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
packages = [{ include = "mxm", from = "." }]
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "fail"
    assert result.code == "PY004"


def test_check_tool_pyright_absent_passes_when_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
""",
    )

    result = check_tool_pyright_absent(tmp_path, "PY031")

    assert result.status == "pass"
    assert result.code == "PY031"
    assert result.path == tmp_path / "pyproject.toml"


def test_check_tool_pyright_absent_fails_when_present(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"

[tool.pyright]
typeCheckingMode = "strict"
""",
    )

    result = check_tool_pyright_absent(tmp_path, "PY031")

    assert result.status == "fail"
    assert result.code == "PY031"
    assert result.path == tmp_path / "pyproject.toml"
    assert result.message == (
        "[tool.pyright] must not be defined; use pyrightconfig.json instead."
    )


def test_check_tool_pyright_absent_fails_when_toml_invalid(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.pyright\n")

    result = check_tool_pyright_absent(tmp_path, "PY031")

    assert result.status == "fail"
    assert result.code == "PY031"
    assert result.path == tmp_path / "pyproject.toml"


def test_check_pyproject_section_exists_passes_when_section_exists(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry.dependencies]
python = ">=3.13,<4.0"
""",
    )

    result = check_pyproject_section_exists(
        tmp_path,
        "PY005",
        ("tool", "poetry", "dependencies"),
        "[tool.poetry.dependencies]",
    )

    assert result.status == "pass"
    assert result.code == "PY005"
    assert result.message == "Found [tool.poetry.dependencies]."


def test_check_pyproject_section_exists_fails_when_section_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, "[tool.poetry]\nname = 'mxm-example'\n")

    result = check_pyproject_section_exists(
        tmp_path,
        "PY005",
        ("tool", "poetry", "dependencies"),
        "[tool.poetry.dependencies]",
    )

    assert result.status == "fail"
    assert result.code == "PY005"
    assert result.message == "Missing [tool.poetry.dependencies] section."


def test_check_poetry_include_contains_package_py_typed_passes_with_string_include(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
include = ["src/mxm/example/py.typed"]
""",
    )

    result = check_poetry_include_contains_package_py_typed(tmp_path, "PY009")

    assert result.status == "pass"
    assert result.code == "PY009"
    assert result.message == "Found py.typed include 'src/mxm/example/py.typed'."


def test_check_poetry_include_contains_package_py_typed_passes_with_mapping_include(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
include = [
  { path = "src/mxm/example/py.typed", format = "wheel" },
]
""",
    )

    result = check_poetry_include_contains_package_py_typed(tmp_path, "PY009")

    assert result.status == "pass"
    assert result.code == "PY009"


def test_check_poetry_include_contains_package_py_typed_supports_hyphen_to_underscore(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example-tools"
include = ["src/mxm/example_tools/py.typed"]
""",
    )

    result = check_poetry_include_contains_package_py_typed(tmp_path, "PY009")

    assert result.status == "pass"
    assert result.code == "PY009"


def test_check_poetry_include_contains_package_py_typed_fails_when_include_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
""",
    )

    result = check_poetry_include_contains_package_py_typed(tmp_path, "PY009")

    assert result.status == "fail"
    assert result.code == "PY009"
    assert result.message == "tool.poetry.include is missing or not a list."


def test_check_poetry_include_contains_package_py_typed_fails_when_wrong_path(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
include = ["src/mxm/wrong/py.typed"]
""",
    )

    result = check_poetry_include_contains_package_py_typed(tmp_path, "PY009")

    assert result.status == "fail"
    assert result.code == "PY009"
    assert result.message == (
        "Expected tool.poetry.include to include 'src/mxm/example/py.typed'."
    )


def test_check_poetry_dependencies_exists_passes(tmp_path: Path) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry.dependencies]
python = ">=3.13,<4.0"
""",
    )

    result = check_poetry_dependencies_exists(tmp_path, "PY005")

    assert result.status == "pass"
    assert result.code == "PY005"


def test_check_poetry_dev_dependencies_exists_passes(tmp_path: Path) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry.group.dev.dependencies]
pytest = "^8.4.2"
""",
    )

    result = check_poetry_dev_dependencies_exists(tmp_path, "PY006")

    assert result.status == "pass"
    assert result.code == "PY006"


def test_check_build_system_exists_passes(tmp_path: Path) -> None:
    write_pyproject(
        tmp_path,
        """
[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
""",
    )

    result = check_build_system_exists(tmp_path, "PY007")

    assert result.status == "pass"
    assert result.code == "PY007"


def test_check_pytest_ini_options_exists_passes(tmp_path: Path) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.pytest.ini_options]
addopts = "-q"
pythonpath = ["src"]
""",
    )

    result = check_pytest_ini_options_exists(tmp_path, "PY008")

    assert result.status == "pass"
    assert result.code == "PY008"


def test_check_mxm_package_matches_poetry_distribution_name_pass(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
""",
    )
    (tmp_path / "src" / "mxm" / "example").mkdir(parents=True)

    result = check_mxm_package_matches_poetry_distribution_name(tmp_path, "PY010")

    assert result.status == "pass"
    assert result.code == "PY010"
    assert result.path == tmp_path / "src" / "mxm" / "example"


def test_check_mxm_package_matches_poetry_distribution_name_supports_hyphen_to_underscore(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example-tools"
""",
    )
    (tmp_path / "src" / "mxm" / "example_tools").mkdir(parents=True)

    result = check_mxm_package_matches_poetry_distribution_name(tmp_path, "PY010")

    assert result.status == "pass"
    assert result.code == "PY010"
    assert result.path == tmp_path / "src" / "mxm" / "example_tools"


def test_check_mxm_package_matches_poetry_distribution_name_fails_when_directory_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example"
""",
    )

    result = check_mxm_package_matches_poetry_distribution_name(tmp_path, "PY010")

    assert result.status == "fail"
    assert result.code == "PY010"
    assert result.path == tmp_path / "src" / "mxm" / "example"


def test_check_mxm_package_matches_poetry_distribution_name_fails_when_name_missing(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
description = "Example"
""",
    )

    result = check_mxm_package_matches_poetry_distribution_name(tmp_path, "PY010")

    assert result.status == "fail"
    assert result.code == "PY010"


def test_check_mxm_package_matches_poetry_distribution_name_fails_when_name_wrong_prefix(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "example"
""",
    )

    result = check_mxm_package_matches_poetry_distribution_name(tmp_path, "PY010")

    assert result.status == "fail"
    assert result.code == "PY010"


def test_pyproject_checks_include_expected_checks() -> None:
    from mxm.foundry.checks.predicates import pyproject

    checks_by_code = {check.code: check for check in pyproject.PYPROJECT_CHECKS}

    expected = {
        "PY001",
        "PY002",
        "PY003",
        "PY004",
        "PY005",
        "PY006",
        "PY007",
        "PY008",
        "PY009",
        "PY010",
        "PY031",
    }

    assert expected.issubset(checks_by_code)
