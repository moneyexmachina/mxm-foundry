from __future__ import annotations

from pathlib import Path

import pytest

from mxm.foundry.checks.models import Check
from mxm.foundry.checks.predicates import makefile
from mxm.foundry.checks.predicates.makefile import (
    canonical_target_commands,
    check_makefile_defines_canonical_target,
    check_makefile_defines_fmt_target,
    check_makefile_defines_lint_target,
    check_makefile_defines_type_target,
    check_makefile_fmt_matches_canonical_commands,
    check_makefile_lint_matches_canonical_commands,
    check_makefile_target_matches_canonical_commands,
    check_makefile_type_matches_canonical_commands,
    target_commands,
)


def write_makefile(project_root: Path, content: str) -> Path:
    path = project_root / "Makefile"
    path.write_text(content, encoding="utf-8")
    return path


def test_target_commands_returns_commands_for_target() -> None:
    contents = """\
lint:
\t$(RUN) ruff check .

type:
\t$(RUN) pyright

test:
\t$(RUN) pytest -q
"""

    assert target_commands(contents, "type") == ["$(RUN) pyright"]


def test_target_commands_returns_empty_list_for_empty_target() -> None:
    contents = """\
type:

test:
\t$(RUN) pytest -q
"""

    assert target_commands(contents, "type") == []


def test_target_commands_returns_none_for_missing_target() -> None:
    contents = """\
test:
\t$(RUN) pytest -q
"""

    assert target_commands(contents, "type") is None


@pytest.mark.parametrize(
    "target_name",
    ["type", "lint", "fmt"],
)
def test_canonical_target_commands_reads_expected_targets(target_name: str) -> None:
    commands, error = canonical_target_commands(target_name)

    assert error is None
    assert commands is not None
    assert commands


@pytest.mark.parametrize(
    ("target_name", "code"),
    [
        ("type", "MK001"),
        ("lint", "MK003"),
        ("fmt", "MK005"),
    ],
)
def test_check_makefile_defines_canonical_target_passes_when_target_exists(
    tmp_path: Path,
    target_name: str,
    code: str,
) -> None:
    write_makefile(
        tmp_path,
        f"""\
{target_name}:
\t@echo ok
""",
    )

    result = check_makefile_defines_canonical_target(tmp_path, code, target_name)

    assert result.status == "pass"
    assert result.code == code
    assert result.path == tmp_path / "Makefile"
    assert result.message == f"Found canonical {target_name} target."


@pytest.mark.parametrize(
    ("target_name", "code"),
    [
        ("type", "MK001"),
        ("lint", "MK003"),
        ("fmt", "MK005"),
    ],
)
def test_check_makefile_defines_canonical_target_fails_when_makefile_is_missing(
    tmp_path: Path,
    target_name: str,
    code: str,
) -> None:
    result = check_makefile_defines_canonical_target(tmp_path, code, target_name)

    assert result.status == "fail"
    assert result.code == code
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile is missing."


@pytest.mark.parametrize(
    ("target_name", "code"),
    [
        ("type", "MK001"),
        ("lint", "MK003"),
        ("fmt", "MK005"),
    ],
)
def test_check_makefile_defines_canonical_target_fails_when_target_is_missing(
    tmp_path: Path,
    target_name: str,
    code: str,
) -> None:
    write_makefile(
        tmp_path,
        """\
test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_defines_canonical_target(tmp_path, code, target_name)

    assert result.status == "fail"
    assert result.code == code
    assert result.path == tmp_path / "Makefile"
    assert result.message == f"Makefile must define canonical {target_name} target."


@pytest.mark.parametrize(
    ("target_name", "code"),
    [
        ("type", "MK002"),
        ("lint", "MK004"),
        ("fmt", "MK006"),
    ],
)
def test_check_makefile_target_matches_canonical_commands_passes_when_commands_match(
    tmp_path: Path,
    target_name: str,
    code: str,
) -> None:
    canonical_commands, error = canonical_target_commands(target_name)

    assert error is None
    assert canonical_commands is not None

    commands_text = "\n".join(f"\t{command}" for command in canonical_commands)
    write_makefile(
        tmp_path,
        f"""\
{target_name}:
{commands_text}
""",
    )

    result = check_makefile_target_matches_canonical_commands(
        tmp_path,
        code,
        target_name,
    )

    assert result.status == "pass"
    assert result.code == code
    assert result.path == tmp_path / "Makefile"
    assert result.message == (
        f"{target_name} target matches canonical Makefile commands."
    )


def test_check_makefile_target_matches_canonical_commands_fails_when_makefile_missing(
    tmp_path: Path,
) -> None:
    result = check_makefile_target_matches_canonical_commands(
        tmp_path,
        "MK002",
        "type",
    )

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == "Makefile is missing."


def test_check_makefile_target_matches_canonical_commands_fails_when_target_missing(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
test:
\t$(RUN) pytest -q
""",
    )

    result = check_makefile_target_matches_canonical_commands(
        tmp_path,
        "MK002",
        "type",
    )

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message == (
        "Cannot compare commands because Makefile canonical type target is missing."
    )


def test_check_makefile_target_matches_canonical_commands_fails_when_commands_differ(
    tmp_path: Path,
) -> None:
    write_makefile(
        tmp_path,
        """\
type:
\tpoetry run pyright
""",
    )

    result = check_makefile_target_matches_canonical_commands(
        tmp_path,
        "MK002",
        "type",
    )

    assert result.status == "fail"
    assert result.code == "MK002"
    assert result.path == tmp_path / "Makefile"
    assert result.message.startswith(
        "type target commands do not match canonical Makefile commands."
    )


def test_specific_makefile_predicates_pass_with_canonical_makefile(
    tmp_path: Path,
) -> None:
    canonical_contents = makefile.POLICY_MAKEFILE_PATH.read_text(encoding="utf-8")
    write_makefile(tmp_path, canonical_contents)

    assert check_makefile_defines_type_target(tmp_path, "MK001").status == "pass"
    assert (
        check_makefile_type_matches_canonical_commands(
            tmp_path,
            "MK002",
        ).status
        == "pass"
    )
    assert check_makefile_defines_lint_target(tmp_path, "MK003").status == "pass"
    assert (
        check_makefile_lint_matches_canonical_commands(
            tmp_path,
            "MK004",
        ).status
        == "pass"
    )
    assert check_makefile_defines_fmt_target(tmp_path, "MK005").status == "pass"
    assert (
        check_makefile_fmt_matches_canonical_commands(
            tmp_path,
            "MK006",
        ).status
        == "pass"
    )


def test_makefile_checks_include_expected_checks() -> None:
    checks_by_code: dict[str, Check] = {
        check.code: check for check in makefile.MAKEFILE_CHECKS
    }

    assert checks_by_code["MK001"].name == "Makefile defines canonical type target"
    assert checks_by_code["MK002"].name == "type target matches canonical commands"
    assert checks_by_code["MK003"].name == "Makefile defines canonical lint target"
    assert checks_by_code["MK004"].name == "lint target matches canonical commands"
    assert checks_by_code["MK005"].name == "Makefile defines canonical fmt target"
    assert checks_by_code["MK006"].name == "fmt target matches canonical commands"
