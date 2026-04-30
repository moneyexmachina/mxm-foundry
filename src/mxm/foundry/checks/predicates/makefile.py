from __future__ import annotations

from pathlib import Path

from mxm.foundry.checks.models import Check, CheckResult

TYPE_TARGET = "type"
CANONICAL_PYRIGHT_COMMANDS = {
    "$(RUN) pyright",
    "$(POETRY) run pyright",
    "poetry run pyright",
}


def _read_makefile(project_root: Path) -> tuple[str | None, Path, str | None]:
    path = project_root / "Makefile"

    try:
        return path.read_text(encoding="utf-8"), path, None
    except FileNotFoundError:
        return None, path, "Makefile is missing."
    except OSError as exc:
        return None, path, f"Could not read Makefile: {exc}"


def _target_commands(contents: str, target_name: str) -> list[str] | None:
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


def check_makefile_defines_type_target(
    project_root: Path,
    code: str,
) -> CheckResult:
    contents, path, error = _read_makefile(project_root)
    if contents is None:
        return CheckResult(
            code=code,
            name="Makefile defines type target",
            status="fail",
            message=error or "Cannot inspect Makefile.",
            path=path,
        )

    commands = _target_commands(contents, TYPE_TARGET)
    if commands is not None:
        return CheckResult(
            code=code,
            name="Makefile defines type target",
            status="pass",
            message="Found type target.",
            path=path,
        )

    return CheckResult(
        code=code,
        name="Makefile defines type target",
        status="fail",
        message="Makefile must define a type target.",
        path=path,
    )


def check_makefile_type_invokes_pyright(
    project_root: Path,
    code: str,
) -> CheckResult:
    contents, path, error = _read_makefile(project_root)
    if contents is None:
        return CheckResult(
            code=code,
            name="type target invokes pyright",
            status="fail",
            message=error or "Cannot inspect Makefile.",
            path=path,
        )

    commands = _target_commands(contents, TYPE_TARGET)
    if commands is None:
        return CheckResult(
            code=code,
            name="type target invokes pyright",
            status="fail",
            message="Cannot inspect pyright invocation because Makefile type target is missing.",
            path=path,
        )

    if not commands:
        return CheckResult(
            code=code,
            name="type target invokes pyright",
            status="fail",
            message="Makefile type target has no commands.",
            path=path,
        )

    for command in commands:
        if command in CANONICAL_PYRIGHT_COMMANDS:
            return CheckResult(
                code=code,
                name="type target invokes pyright",
                status="pass",
                message=f"type target invokes canonical pyright command: {command!r}.",
                path=path,
            )

    return CheckResult(
        code=code,
        name="type target invokes pyright",
        status="fail",
        message="Makefile type target must invoke one of: "
        + ", ".join(sorted(repr(command) for command in CANONICAL_PYRIGHT_COMMANDS)),
        path=path,
    )


MAKEFILE_CHECKS: tuple[Check, ...] = (
    Check(
        code="MK001",
        name="Makefile defines type target",
        run=lambda root: check_makefile_defines_type_target(root, "MK001"),
    ),
    Check(
        code="MK002",
        name="type target invokes pyright",
        run=lambda root: check_makefile_type_invokes_pyright(root, "MK002"),
    ),
)
