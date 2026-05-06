from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from mxm.foundry.cli import app

runner = CliRunner()


def test_check_cli_valid_project(minimal_valid_project: Path) -> None:
    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 0
    assert "MXM Foundry Check:" in result.stdout
    assert "[POLICY] License policy" in result.stdout
    assert "[POLICY] Typing policy" in result.stdout
    assert "[POLICY] Formatting policy" in result.stdout
    assert "[POLICY] Pyproject policy" in result.stdout
    assert "[POLICY] Testing policy" in result.stdout
    assert "[POLICY] Check gate policy" in result.stdout
    assert "[POLICY] Documentation policy" in result.stdout
    assert "PASS POLICY_TYPING Typing policy" in result.stdout
    assert "PASS FS002" in result.stdout
    assert "PASS LIC001" in result.stdout
    assert "PASS POLICY_LICENSE License policy" in result.stdout
    assert "PASS POLICY_PYPROJECT Pyproject policy" in result.stdout
    assert "PASS POLICY_TESTING Testing policy" in result.stdout
    assert "PASS POLICY_CHECK_GATE Check gate policy" in result.stdout
    assert "PASS POLICY_DOCUMENTATION Documentation policy" in result.stdout


def test_check_cli_invalid_project(minimal_valid_project: Path) -> None:
    (minimal_valid_project / "README.md").unlink()

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] Documentation policy" in result.stdout
    assert "FAIL FS001" in result.stdout
    assert "README.md exists" in result.stdout


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


def test_check_cli_missing_path(tmp_path: Path) -> None:
    missing_path = tmp_path / "does-not-exist"

    result = runner.invoke(app, ["check", str(missing_path)])

    assert result.exit_code == 1
    assert "Path does not exist" in result.stdout


def test_check_cli_invalid_typing_policy_when_tool_pyright_present(
    minimal_valid_project: Path,
) -> None:
    pyproject = minimal_valid_project / "pyproject.toml"
    pyproject.write_text(
        pyproject.read_text(encoding="utf-8")
        + '\n[tool.pyright]\ntypeCheckingMode = "strict"\n',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] Typing policy" in result.stdout
    assert "FAIL PY031" in result.stdout
    assert "[tool.pyright] is absent" in result.stdout
    assert "FAIL POLICY_TYPING Typing policy" in result.stdout


def test_check_cli_invalid_typing_policy_when_makefile_type_target_missing(
    minimal_valid_project: Path,
) -> None:
    makefile = minimal_valid_project / "Makefile"
    makefile.write_text(
        ".PHONY: test check\n\n"
        "test:\n"
        "\tpoetry run pytest\n\n"
        "check:\n"
        "\tpoetry run pytest\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["check", str(minimal_valid_project)])

    assert result.exit_code == 1
    assert "[POLICY] Typing policy" in result.stdout
    assert "FAIL MK001" in result.stdout
    assert "FAIL MK002" in result.stdout
    assert "FAIL POLICY_TYPING Typing policy" in result.stdout
