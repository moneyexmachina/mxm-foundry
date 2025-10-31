from __future__ import annotations

from typer.testing import CliRunner

from mxm.foundry import __version__
from mxm.foundry.cli import app

runner = CliRunner()


def test_version_string() -> None:
    assert isinstance(__version__, str)
    assert __version__  # non-empty


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout or "Usage:" in result.stdout


def test_cli_new_stub() -> None:
    # Adjust this assertion later when `new` writes files.
    result = runner.invoke(app, ["new", "example"])
    assert result.exit_code == 0
    # The stub prints a confirmation line; keep this loose for now.
    assert "mxm-example" in result.stdout
