# tests/checks/predicates/test_makefile.py

from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates import makefile
from mxm.foundry.checks.predicates.makefile import (
    check_makefile_defines_type_target,
    check_makefile_type_invokes_pyright,
)


def write_makefile(project_root: Path, content: str) -> Path:
    path = project_root / "Makefile"
    path.write_text(content, encoding="utf-8")
    return path


def test_check_makefile_defines_type_target_passes_when_type_target_exists(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:
\t$(RUN) pyright
""",
    )

    result = check_makefile_defines_type_target(tmp_path, "MK001")

    assert result.status == "pass"
    assert result.code == "MK001"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Found type target."


def test_check_makefile_defines_type_target_fails_when_makefile_is_missing(
    tmp_path: Path,
) -> None:
    result = check_makefile_defines_type_target(tmp_path, "MK001")

    assert result.status == "fail"
    assert result.code == "MK001"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile is missing."


def test_check_makefile_defines_type_target_fails_when_type_target_is_missing(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_defines_type_target(tmp_path, "MK001")

    assert result.status == "fail"
    assert result.code == "MK001"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile must define a type target."


def test_check_makefile_type_invokes_pyright_passes_with_run_variable(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
POETRY ?= poetry
RUN     = $(POETRY) run

type:
\t$(RUN) pyright
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "pass"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert (
        result.message
        == "type target invokes canonical pyright command: '$(RUN) pyright'."
    )


def test_check_makefile_type_invokes_pyright_passes_with_poetry_variable(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:
\t$(POETRY) run pyright
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "pass"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == (
        "type target invokes canonical pyright command: '$(POETRY) run pyright'."
    )


def test_check_makefile_type_invokes_pyright_passes_with_literal_poetry(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:
\tpoetry run pyright
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "pass"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert (
        result.message
        == "type target invokes canonical pyright command: 'poetry run pyright'."
    )


def test_check_makefile_type_invokes_pyright_fails_when_makefile_is_missing(
    tmp_path: Path,
) -> None:
    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile is missing."


def test_check_makefile_type_invokes_pyright_fails_when_type_target_is_missing(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == (
        "Cannot inspect pyright invocation because Makefile type target is missing."
    )


def test_check_makefile_type_invokes_pyright_fails_when_type_target_has_no_commands(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:

test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile type target has no commands."


def test_check_makefile_type_invokes_pyright_fails_when_command_is_wrong(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:
\tpyright
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message.startswith("Makefile type target must invoke one of: ")


def test_check_makefile_type_invokes_pyright_only_reads_type_target(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
lint:
\t$(RUN) pyright

type:
\t$(RUN) mypy

test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_type_invokes_pyright(tmp_path, "MK002")

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"


def test_makefile_checks_include_type_target_and_pyright_invocation_checks() -> None:
    checks_by_code: dict[str, Check] = {
        check.code: check for check in makefile.MAKEFILE_CHECKS
    }

    assert "MK001" in checks_by_code
    assert checks_by_code["MK001"].name == "Makefile defines type target"

    assert "MK002" in checks_by_code
    assert checks_by_code["MK002"].name == "type target invokes pyright"
