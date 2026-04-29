from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult, Policy
from mxm.foundry.checks.runner import (
    run_checks,
    run_misc_checks,
    run_policies,
    run_policy,
)
from tests.checks.expected import EXPECTED_CHECK_CODES


def test_run_checks_valid_minimal_project(
    minimal_valid_project: Path,
) -> None:
    results = run_checks(minimal_valid_project)
    assert results

    assert {result.code for result in results} == set(EXPECTED_CHECK_CODES)
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

    assert [result.code for result in results] == EXPECTED_CHECK_CODES


def test_run_policy_runs_all_checks_and_aggregates_pass_status(
    tmp_path: Path,
) -> None:
    policy = Policy(
        code="POLICY_TEST",
        name="Test policy",
        checks=(
            Check(
                code="A",
                name="A",
                run=lambda root: CheckResult(
                    code="A",
                    name="A",
                    status="pass",
                    message="ok",
                    path=root / "a",
                ),
            ),
            Check(
                code="B",
                name="B",
                run=lambda root: CheckResult(
                    code="B",
                    name="B",
                    status="pass",
                    message="ok",
                    path=root / "b",
                ),
            ),
        ),
    )

    result = run_policy(policy, tmp_path)

    assert result.code == "POLICY_TEST"
    assert result.name == "Test policy"
    assert result.status == "pass"
    assert [check.code for check in result.checks] == ["A", "B"]


def test_run_policy_fails_when_any_check_fails(tmp_path: Path) -> None:
    policy = Policy(
        code="POLICY_TEST",
        name="Test policy",
        checks=(
            Check(
                code="A",
                name="A",
                run=lambda root: CheckResult(
                    code="A",
                    name="A",
                    status="pass",
                    message="ok",
                ),
            ),
            Check(
                code="B",
                name="B",
                run=lambda root: CheckResult(
                    code="B",
                    name="B",
                    status="fail",
                    message="bad",
                ),
            ),
        ),
    )

    result = run_policy(policy, tmp_path)

    assert result.status == "fail"


def test_run_policies_valid_minimal_project(
    minimal_valid_project: Path,
) -> None:
    results = run_policies(minimal_valid_project)

    assert [result.code for result in results] == ["POLICY_LICENSE"]
    assert all(result.status == "pass" for result in results)


def test_run_policies_license_policy_fails_when_license_missing(
    minimal_valid_project: Path,
) -> None:
    (minimal_valid_project / "LICENSE").unlink()

    results = run_policies(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    license_policy = result_by_code["POLICY_LICENSE"]

    assert license_policy.status == "fail"
    assert [check.code for check in license_policy.checks] == ["FS002", "LIC001"]
    assert all(check.status == "fail" for check in license_policy.checks)


def test_run_policies_license_policy_fails_when_license_differs(
    minimal_valid_project: Path,
) -> None:
    (minimal_valid_project / "LICENSE").write_text(
        "not the canonical license\n",
        encoding="utf-8",
    )

    results = run_policies(minimal_valid_project)
    result_by_code = {result.code: result for result in results}

    license_policy = result_by_code["POLICY_LICENSE"]

    assert license_policy.status == "fail"
    assert [check.code for check in license_policy.checks] == ["FS002", "LIC001"]

    check_by_code = {check.code: check for check in license_policy.checks}
    assert check_by_code["FS002"].status == "pass"
    assert check_by_code["LIC001"].status == "fail"


def test_run_misc_checks_excludes_policy_covered_checks(
    minimal_valid_project: Path,
) -> None:
    results = run_misc_checks(minimal_valid_project)
    codes = [result.code for result in results]

    assert "FS002" not in codes
    assert "LIC001" not in codes
    assert "FS001" in codes
    assert all(result.status == "pass" for result in results)
