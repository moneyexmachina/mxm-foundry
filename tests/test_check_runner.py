from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.runner import run_checks


def test_run_checks_valid_minimal_project(
    minimal_project: Path,
) -> None:
    results = run_checks(minimal_project)

    assert results
    assert {result.code for result in results} == {
        "FS001",
        "FS002",
        "FS003",
        "FS004",
        "FS005",
    }
    assert all(result.status == "pass" for result in results)


def test_run_checks_missing_required_file(
    minimal_project: Path,
) -> None:
    (minimal_project / "README.md").unlink()

    results = run_checks(minimal_project)

    result_by_code = {result.code: result for result in results}

    assert result_by_code["FS001"].status == "fail"
    assert result_by_code["FS001"].path == minimal_project / "README.md"


def test_run_checks_uses_deterministic_order(
    minimal_project: Path,
) -> None:
    results = run_checks(minimal_project)

    assert [result.code for result in results] == [
        "FS001",
        "FS002",
        "FS003",
        "FS004",
        "FS005",
    ]
