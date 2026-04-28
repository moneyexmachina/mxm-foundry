from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from mxm.foundry.cli import app

runner = CliRunner()


def test_check_cli_valid_project(minimal_valid_project: Path) -> None:
    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 0
    assert "PASS=15" in result.stdout
    assert "FAIL=0" in result.stdout


def test_check_cli_invalid_project(minimal_valid_project: Path) -> None:
    (minimal_valid_project / "README.md").unlink()

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "FS001" in result.stdout
    assert "FAIL=1" in result.stdout


def test_check_cli_missing_path(tmp_path: Path) -> None:
    missing_path = tmp_path / "does-not-exist"

    result = runner.invoke(app, ["check", str(missing_path)])

    assert result.exit_code == 1
    assert "Path does not exist" in result.stdout
