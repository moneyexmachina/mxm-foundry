from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.predicates.pyproject import (
    check_poetry_name_starts_with_mxm,
    check_poetry_package_uses_src_mxm_layout,
    check_pyproject_parseable,
    check_tool_poetry_exists,
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
packages = [{ include = "mxm/example", from = "src" }]
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "pass"
    assert result.code == "PY004"


def test_check_poetry_package_uses_src_mxm_layout_supports_hyphen_to_underscore(
    tmp_path: Path,
) -> None:
    write_pyproject(
        tmp_path,
        """
[tool.poetry]
name = "mxm-example-tools"
packages = [{ include = "mxm/example_tools", from = "src" }]
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
packages = [{ include = "mxm/wrong", from = "src" }]
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
packages = [{ include = "mxm/example", from = "." }]
""",
    )

    result = check_poetry_package_uses_src_mxm_layout(tmp_path, "PY004")

    assert result.status == "fail"
    assert result.code == "PY004"
