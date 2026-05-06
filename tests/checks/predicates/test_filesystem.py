from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.predicates.filesystem import (
    check_package_py_typed,
    check_required_directory,
    check_required_file,
    check_single_mxm_package,
    check_src_mxm_is_namespace_package,
)


def test_check_required_file_pass(tmp_path: Path) -> None:
    file_path = tmp_path / "README.md"
    file_path.write_text("# Test\n")

    result = check_required_file(tmp_path, "README.md", "FS001")

    assert result.status == "pass"
    assert result.code == "FS001"
    assert result.path == file_path


def test_check_required_file_fail(tmp_path: Path) -> None:
    result = check_required_file(tmp_path, "README.md", "FS001")

    assert result.status == "fail"
    assert result.code == "FS001"
    assert result.path == tmp_path / "README.md"


def test_check_required_file_different_file(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").write_text("MIT\n")

    result = check_required_file(tmp_path, "LICENSE", "FS002")

    assert result.status == "pass"
    assert result.code == "FS002"
    assert result.path == tmp_path / "LICENSE"


def test_check_required_directory_pass(tmp_path: Path) -> None:
    directory_path = tmp_path / "tests"
    directory_path.mkdir()

    result = check_required_directory(tmp_path, "tests", "FS006")

    assert result.status == "pass"
    assert result.code == "FS006"
    assert result.path == directory_path


def test_check_required_directory_fail(tmp_path: Path) -> None:
    result = check_required_directory(tmp_path, "tests", "FS006")

    assert result.status == "fail"
    assert result.code == "FS006"
    assert result.path == tmp_path / "tests"


def test_check_single_mxm_package_pass(tmp_path: Path) -> None:
    package_path = tmp_path / "src" / "mxm" / "example"
    package_path.mkdir(parents=True)

    result = check_single_mxm_package(tmp_path, "FS008")

    assert result.status == "pass"
    assert result.code == "FS008"
    assert result.path == package_path


def test_check_single_mxm_package_fails_when_src_mxm_missing(tmp_path: Path) -> None:
    result = check_single_mxm_package(tmp_path, "FS008")

    assert result.status == "fail"
    assert result.code == "FS008"
    assert result.path == tmp_path / "src" / "mxm"


def test_check_single_mxm_package_fails_when_no_package_exists(tmp_path: Path) -> None:
    mxm_root = tmp_path / "src" / "mxm"
    mxm_root.mkdir(parents=True)

    result = check_single_mxm_package(tmp_path, "FS008")

    assert result.status == "fail"
    assert result.code == "FS008"
    assert result.path == mxm_root


def test_check_single_mxm_package_fails_when_multiple_packages_exist(
    tmp_path: Path,
) -> None:
    mxm_root = tmp_path / "src" / "mxm"
    (mxm_root / "example").mkdir(parents=True)
    (mxm_root / "other").mkdir()

    result = check_single_mxm_package(tmp_path, "FS008")

    assert result.status == "fail"
    assert result.code == "FS008"
    assert result.path == mxm_root


def test_check_package_py_typed_pass(tmp_path: Path) -> None:
    package_path = tmp_path / "src" / "mxm" / "example"
    package_path.mkdir(parents=True)
    py_typed_path = package_path / "py.typed"
    py_typed_path.write_text("")

    result = check_package_py_typed(tmp_path, "FS009")

    assert result.status == "pass"
    assert result.code == "FS009"
    assert result.path == py_typed_path


def test_check_package_py_typed_fails_when_src_mxm_missing(tmp_path: Path) -> None:
    result = check_package_py_typed(tmp_path, "FS009")

    assert result.status == "fail"
    assert result.code == "FS009"
    assert result.path == tmp_path / "src" / "mxm"


def test_check_package_py_typed_fails_when_multiple_packages_exist(
    tmp_path: Path,
) -> None:
    mxm_root = tmp_path / "src" / "mxm"
    (mxm_root / "example").mkdir(parents=True)
    (mxm_root / "other").mkdir()

    result = check_package_py_typed(tmp_path, "FS009")

    assert result.status == "fail"
    assert result.code == "FS009"
    assert result.path == mxm_root


def test_check_package_py_typed_fails_when_marker_missing(tmp_path: Path) -> None:
    package_path = tmp_path / "src" / "mxm" / "example"
    package_path.mkdir(parents=True)

    result = check_package_py_typed(tmp_path, "FS009")

    assert result.status == "fail"
    assert result.code == "FS009"
    assert result.path == package_path / "py.typed"


def test_check_src_mxm_is_namespace_package_passes_without_init(
    tmp_path: Path,
) -> None:
    mxm_root = tmp_path / "src" / "mxm"
    mxm_root.mkdir(parents=True)

    result = check_src_mxm_is_namespace_package(tmp_path, "FS011")

    assert result.status == "pass"
    assert result.code == "FS011"
    assert result.path == mxm_root


def test_check_src_mxm_is_namespace_package_fails_when_src_mxm_missing(
    tmp_path: Path,
) -> None:
    result = check_src_mxm_is_namespace_package(tmp_path, "FS011")

    assert result.status == "fail"
    assert result.code == "FS011"
    assert result.path == tmp_path / "src" / "mxm"


def test_check_src_mxm_is_namespace_package_fails_when_init_exists(
    tmp_path: Path,
) -> None:
    mxm_root = tmp_path / "src" / "mxm"
    mxm_root.mkdir(parents=True)
    init_path = mxm_root / "__init__.py"
    init_path.write_text("")

    result = check_src_mxm_is_namespace_package(tmp_path, "FS011")

    assert result.status == "fail"
    assert result.code == "FS011"
    assert result.path == init_path
