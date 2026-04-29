from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import (
    Check,
    CheckResult,
    Policy,
    PolicyResult,
    aggregate_check_status,
)


def test_check_result_can_include_path() -> None:
    path = Path("pyrightconfig.json")

    result = CheckResult(
        code="PY030",
        name="pyrightconfig.json matches canonical config",
        status="pass",
        message="ok",
        path=path,
    )

    assert result.path == path


def test_policy_groups_checks_without_running_them() -> None:
    check = Check(
        code="FS002",
        name="LICENSE exists",
        run=lambda root: CheckResult(
            code="FS002",
            name="LICENSE exists",
            status="pass",
            message="ok",
            path=root / "LICENSE",
        ),
    )

    policy = Policy(
        code="POLICY_LICENSE",
        name="License policy",
        checks=(check,),
    )

    assert policy.code == "POLICY_LICENSE"
    assert policy.name == "License policy"
    assert policy.checks == (check,)


def test_policy_result_contains_aggregate_status_and_check_results() -> None:
    check_result = CheckResult(
        code="FS002",
        name="LICENSE exists",
        status="pass",
        message="ok",
        path=Path("LICENSE"),
    )

    result = PolicyResult(
        code="POLICY_LICENSE",
        name="License policy",
        status="pass",
        checks=(check_result,),
    )

    assert result.status == "pass"
    assert result.checks == (check_result,)


def test_aggregate_check_status_passes_when_all_checks_pass() -> None:
    results = (
        CheckResult(code="A", name="A", status="pass", message="ok"),
        CheckResult(code="B", name="B", status="pass", message="ok"),
    )

    assert aggregate_check_status(results) == "pass"


def test_aggregate_check_status_fails_when_any_check_fails() -> None:
    results = (
        CheckResult(code="A", name="A", status="pass", message="ok"),
        CheckResult(code="B", name="B", status="fail", message="bad"),
    )

    assert aggregate_check_status(results) == "fail"


def test_aggregate_check_status_fails_when_any_check_warns() -> None:
    results = (
        CheckResult(code="A", name="A", status="pass", message="ok"),
        CheckResult(code="B", name="B", status="warn", message="warning"),
    )

    assert aggregate_check_status(results) == "fail"


def test_aggregate_check_status_passes_for_empty_results() -> None:
    assert aggregate_check_status(()) == "pass"
