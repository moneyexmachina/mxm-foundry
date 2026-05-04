from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult

POLICY_MAKEFILE_PATH = Path(__file__).parents[2] / "canonical" / "Makefile"

TYPE_TARGET = "type"
LINT_TARGET = "lint"
FMT_TARGET = "fmt"
TEST_TARGET = "test"


def read_makefile_path(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"{path.name} is missing."
    except OSError as exc:
        return None, f"Could not read {path.name}: {exc}"


def read_project_makefile(project_root: Path) -> tuple[str | None, Path, str | None]:
    path = project_root / "Makefile"
    contents, error = read_makefile_path(path)
    return contents, path, error


def target_commands(contents: str, target_name: str) -> list[str] | None:
    lines = contents.splitlines()
    in_target = False
    commands: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if not line.startswith(("\t", " ")):
            if stripped == f"{target_name}:":
                in_target = True
                continue

            if in_target:
                break

            continue

        if in_target:
            commands.append(stripped)

    if not in_target:
        return None

    return commands


def canonical_target_commands(target_name: str) -> tuple[list[str] | None, str | None]:
    contents, error = read_makefile_path(POLICY_MAKEFILE_PATH)
    if contents is None:
        return None, error or "Cannot inspect canonical Makefile."

    commands = target_commands(contents, target_name)
    if commands is None:
        return None, f"Canonical Makefile is missing {target_name} target."

    return commands, None


def check_makefile_defines_canonical_target(
    project_root: Path,
    code: str,
    target_name: str,
) -> CheckResult:
    name = f"Makefile defines canonical {target_name} target"

    project_contents, project_path, project_error = read_project_makefile(project_root)
    if project_contents is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=project_error or "Cannot inspect Makefile.",
            path=project_path,
        )

    canonical_commands, canonical_error = canonical_target_commands(target_name)
    if canonical_commands is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=canonical_error or "Cannot inspect canonical Makefile.",
            path=POLICY_MAKEFILE_PATH,
        )

    project_commands = target_commands(project_contents, target_name)
    if project_commands is not None:
        return CheckResult(
            code=code,
            name=name,
            status="pass",
            message=f"Found canonical {target_name} target.",
            path=project_path,
        )

    return CheckResult(
        code=code,
        name=name,
        status="fail",
        message=f"Makefile must define canonical {target_name} target.",
        path=project_path,
    )


def check_makefile_target_matches_canonical_commands(
    project_root: Path,
    code: str,
    target_name: str,
) -> CheckResult:
    name = f"{target_name} target matches canonical commands"

    project_contents, project_path, project_error = read_project_makefile(project_root)
    if project_contents is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=project_error or "Cannot inspect Makefile.",
            path=project_path,
        )

    canonical_commands, canonical_error = canonical_target_commands(target_name)
    if canonical_commands is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=canonical_error or "Cannot inspect canonical Makefile.",
            path=POLICY_MAKEFILE_PATH,
        )

    project_commands = target_commands(project_contents, target_name)
    if project_commands is None:
        return CheckResult(
            code=code,
            name=name,
            status="fail",
            message=(
                f"Cannot compare commands because Makefile canonical "
                f"{target_name} target is missing."
            ),
            path=project_path,
        )

    if project_commands == canonical_commands:
        return CheckResult(
            code=code,
            name=name,
            status="pass",
            message=f"{target_name} target matches canonical Makefile commands.",
            path=project_path,
        )

    return CheckResult(
        code=code,
        name=name,
        status="fail",
        message=(
            f"{target_name} target commands do not match canonical Makefile "
            f"commands. Expected {canonical_commands!r}; found {project_commands!r}."
        ),
        path=project_path,
    )


def check_makefile_defines_type_target(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_defines_canonical_target(project_root, code, TYPE_TARGET)


def check_makefile_type_matches_canonical_commands(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_target_matches_canonical_commands(
        project_root,
        code,
        TYPE_TARGET,
    )


def check_makefile_defines_lint_target(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_defines_canonical_target(project_root, code, LINT_TARGET)


def check_makefile_lint_matches_canonical_commands(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_target_matches_canonical_commands(
        project_root,
        code,
        LINT_TARGET,
    )


def check_makefile_defines_fmt_target(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_defines_canonical_target(project_root, code, FMT_TARGET)


def check_makefile_fmt_matches_canonical_commands(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_target_matches_canonical_commands(
        project_root,
        code,
        FMT_TARGET,
    )


def check_makefile_defines_test_target(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_defines_canonical_target(project_root, code, TEST_TARGET)


def check_makefile_test_matches_canonical_commands(
    project_root: Path,
    code: str,
) -> CheckResult:
    return check_makefile_target_matches_canonical_commands(
        project_root,
        code,
        TEST_TARGET,
    )


MAKEFILE_CHECKS: tuple[Check, ...] = (
    Check(
        code="MK001",
        name="Makefile defines canonical type target",
        run=lambda root: check_makefile_defines_type_target(root, "MK001"),
    ),
    Check(
        code="MK002",
        name="type target matches canonical commands",
        run=lambda root: check_makefile_type_matches_canonical_commands(root, "MK002"),
    ),
    Check(
        code="MK003",
        name="Makefile defines canonical lint target",
        run=lambda root: check_makefile_defines_lint_target(root, "MK003"),
    ),
    Check(
        code="MK004",
        name="lint target matches canonical commands",
        run=lambda root: check_makefile_lint_matches_canonical_commands(root, "MK004"),
    ),
    Check(
        code="MK005",
        name="Makefile defines canonical fmt target",
        run=lambda root: check_makefile_defines_fmt_target(root, "MK005"),
    ),
    Check(
        code="MK006",
        name="fmt target matches canonical commands",
        run=lambda root: check_makefile_fmt_matches_canonical_commands(root, "MK006"),
    ),
    Check(
        code="MK007",
        name="Makefile defines canonical test target",
        run=lambda root: check_makefile_defines_test_target(root, "MK007"),
    ),
    Check(
        code="MK008",
        name="test target matches canonical commands",
        run=lambda root: check_makefile_test_matches_canonical_commands(root, "MK008"),
    ),
)
