from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.runner import run_checks


def test_run_checks_valid_minimal_project(
    minimal_valid_project: Path,
) -> None:
    results = run_checks(minimal_valid_project)

    assert results
    assert {result.code for result in results} == {
        "FS001",
        "FS002",
        "FS003",
        "FS004",
        "FS005",
        "FS006",
        "FS007",
        "FS008",
        "FS009",
        "PY001",
        "PY002",
        "PY003",
        "PY004",
        "PY020",
    }
    assert all(result.status == "pass" for result in results)


def test_run_checks_missing_required_file(
    minimal_valid_project: Path,
) -> None:
    (minimal_valid_project / "README.md").unlink()

    results = run_checks(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS001"].status == "fail"
    assert result_by_code["FS001"].path == minimal_valid_project / "README.md"


def test_run_checks_missing_tests_directory(
    minimal_valid_project: Path,
) -> None:
    (minimal_valid_project / "tests").rmdir()

    results = run_checks(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS006"].status == "fail"
    assert result_by_code["FS006"].path == minimal_valid_project / "tests"


def test_run_checks_missing_src_mxm_directory(
    minimal_valid_project: Path,
) -> None:
    package_root = minimal_valid_project / "src" / "mxm" / "example"
    (package_root / "py.typed").unlink()
    (package_root / "__init__.py").unlink()
    package_root.rmdir()
    (minimal_valid_project / "src" / "mxm").rmdir()

    results = run_checks(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS007"].status == "fail"
    assert result_by_code["FS008"].status == "fail"
    assert result_by_code["FS009"].status == "fail"


def test_run_checks_multiple_mxm_package_directories(
    minimal_valid_project: Path,
) -> None:
    second_package = minimal_valid_project / "src" / "mxm" / "other"
    second_package.mkdir()
    (second_package / "__init__.py").write_text("")
    (second_package / "py.typed").write_text("")

    results = run_checks(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS008"].status == "fail"
    assert result_by_code["FS009"].status == "fail"


def test_run_checks_missing_py_typed(
    minimal_valid_project: Path,
) -> None:
    py_typed = minimal_valid_project / "src" / "mxm" / "example" / "py.typed"
    py_typed.unlink()

    results = run_checks(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS009"].status == "fail"
    assert result_by_code["FS009"].path == py_typed


def test_run_checks_uses_deterministic_order(
    minimal_valid_project: Path,
) -> None:
    results = run_checks(minimal_valid_project)

    assert [result.code for result in results] == [
        "FS001",
        "FS002",
        "FS003",
        "FS004",
        "FS005",
        "FS006",
        "FS007",
        "FS008",
        "FS009",
        "PY001",
        "PY002",
        "PY003",
        "PY004",
        "PY020",
    ]
