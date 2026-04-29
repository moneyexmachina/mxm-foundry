from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from mxm.foundry.cli import app
from tests.checks.expected import EXPECTED_CHECK_COUNT

runner = CliRunner()

EXPECTED_POLICY_COUNT = 2  # LICENSE_POLICY + POLICY_MISC


def test_check_cli_valid_project(minimal_valid_project: Path) -> None:
    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 0
    assert "MXM Foundry Check:" in result.stdout
    assert "[POLICY] License policy" in result.stdout
    assert "[POLICY] Other checks" in result.stdout
    assert "PASS FS002" in result.stdout
    assert "PASS LIC001" in result.stdout
    assert "PASS POLICY_LICENSE License policy" in result.stdout
    assert "PASS POLICY_MISC Other checks" in result.stdout
    assert f"CHECKS(PASS={EXPECTED_CHECK_COUNT} WARN=0 FAIL=0)" in result.stdout
    assert f"POLICIES(PASS={EXPECTED_POLICY_COUNT} FAIL=0)" in result.stdout


def test_check_cli_invalid_project(minimal_valid_project: Path) -> None:
    (minimal_valid_project / "README.md").unlink()

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] Other checks" in result.stdout
    assert "FAIL FS001" in result.stdout
    assert "README.md exists" in result.stdout
    assert f"CHECKS(PASS={EXPECTED_CHECK_COUNT - 1} WARN=0 FAIL=1)" in result.stdout
    assert "POLICIES(PASS=1 FAIL=1)" in result.stdout


def test_check_cli_invalid_license_policy(minimal_valid_project: Path) -> None:
    (minimal_valid_project / "LICENSE").write_text(
        "not the canonical license\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] License policy" in result.stdout
    assert "PASS FS002" in result.stdout
    assert "FAIL LIC001" in result.stdout
    assert "FAIL POLICY_LICENSE License policy" in result.stdout
    assert f"CHECKS(PASS={EXPECTED_CHECK_COUNT - 1} WARN=0 FAIL=1)" in result.stdout
    assert "POLICIES(PASS=1 FAIL=1)" in result.stdout


def test_check_cli_missing_license_file_fails_both_license_checks(
    minimal_valid_project: Path,
) -> None:
    (minimal_valid_project / "LICENSE").unlink()

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] License policy" in result.stdout
    assert "FAIL FS002" in result.stdout
    assert "FAIL LIC001" in result.stdout
    assert "FAIL POLICY_LICENSE License policy" in result.stdout
    assert f"CHECKS(PASS={EXPECTED_CHECK_COUNT - 2} WARN=0 FAIL=2)" in result.stdout
    assert "POLICIES(PASS=1 FAIL=1)" in result.stdout


def test_check_cli_missing_path(tmp_path: Path) -> None:
    missing_path = tmp_path / "does-not-exist"

    result = runner.invoke(app, ["check", str(missing_path)])

    assert result.exit_code == 1
    assert "Path does not exist" in result.stdout
