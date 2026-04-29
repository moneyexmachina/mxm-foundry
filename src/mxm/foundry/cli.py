from __future__ import annotations

from pathlib import Path
from textwrap import wrap
from typing import Annotated, Literal

import typer
from rich.console import Console
from rich.markup import escape

from mxm.foundry.checks.models import CheckResult, PolicyResult
from mxm.foundry.checks.runner import run_misc_checks, run_policies

CODE_WIDTH = 7
CONTINUATION_INDENT = " " * (2 + 4 + 1 + CODE_WIDTH + 1)


app = typer.Typer(
    add_completion=False,
    help="MXM package scaffolding, checks, and sync.",
)

foundry_app = typer.Typer(
    add_completion=False,
    help="Package scaffolding and checks.",
)

console = Console()


def status_label(status: str) -> str:
    """Return a Rich-formatted status label."""

    if status == "pass":
        return "[green]PASS[/]"
    if status == "warn":
        return "[yellow]WARN[/]"
    return "[red]FAIL[/]"


def aggregate_misc_status(
    results: list[CheckResult],
) -> Literal["pass", "fail"]:
    """Aggregate misc check results into a pseudo-policy status."""

    return "pass" if all(result.status == "pass" for result in results) else "fail"


def print_wrapped_line(line: str, *, continuation_indent: str) -> None:
    """Print a line with deterministic continuation indentation."""

    width = console.width
    wrapped = wrap(
        line,
        width=width,
        subsequent_indent=continuation_indent,
        break_long_words=False,
        break_on_hyphens=False,
    )

    for wrapped_line in wrapped or [""]:
        console.print(wrapped_line)


def render_policy_footer(code: str, name: str, status: str) -> None:
    """Render one policy aggregate result line."""

    line = f"  {status_label(status)} {code:<{CODE_WIDTH}} {escape(name)}"
    print_wrapped_line(line, continuation_indent=CONTINUATION_INDENT)


def render_check_line(result: CheckResult) -> None:
    """Render one atomic check result as a log-style line."""

    line = (
        f"  {status_label(result.status)} "
        f"{result.code:<{CODE_WIDTH}} "
        f"{escape(result.name)}"
    )

    if result.status != "pass":
        line = f"{line} -> {escape(result.message)}"

    print_wrapped_line(line, continuation_indent=CONTINUATION_INDENT)


def render_policy_block(policy_result: PolicyResult) -> None:
    """Render one policy result as a log-style block."""

    console.print(f"[bold][POLICY][/bold] {escape(policy_result.name)}")

    for check_result in policy_result.checks:
        render_check_line(check_result)

    render_policy_footer(
        policy_result.code,
        policy_result.name,
        policy_result.status,
    )


def render_misc_block(results: list[CheckResult]) -> Literal["pass", "fail"] | None:
    """Render checks not covered by any registered policy."""

    if not results:
        return None

    status = aggregate_misc_status(results)

    console.print("[bold][POLICY][/bold] Other checks")

    for result in results:
        render_check_line(result)

    render_policy_footer("POLICY_MISC", "Other checks", status)

    return status


def render_check_results(path: Path) -> None:
    """Render the canonical MXM foundry check report."""

    project_root = path.resolve()

    if not project_root.exists():
        console.print(f"[bold red]Error:[/] Path does not exist: {project_root}")
        raise typer.Exit(code=1)

    policy_results = run_policies(project_root)
    misc_results = run_misc_checks(project_root)

    console.print(f"[bold]MXM Foundry Check:[/] {project_root}")

    for policy_result in policy_results:
        console.print()
        render_policy_block(policy_result)

    misc_status: Literal["pass", "fail"] | None = None
    if misc_results:
        console.print()
        misc_status = render_misc_block(misc_results)

    displayed_check_results = [
        check_result
        for policy_result in policy_results
        for check_result in policy_result.checks
    ] + misc_results

    pass_count = sum(result.status == "pass" for result in displayed_check_results)
    warn_count = sum(result.status == "warn" for result in displayed_check_results)
    fail_count = sum(result.status == "fail" for result in displayed_check_results)

    policy_pass_count = sum(result.status == "pass" for result in policy_results)
    policy_fail_count = sum(result.status == "fail" for result in policy_results)

    if misc_status == "pass":
        policy_pass_count += 1
    elif misc_status == "fail":
        policy_fail_count += 1

    console.print()
    console.print(
        "Summary: "
        f"CHECKS(PASS={pass_count} WARN={warn_count} FAIL={fail_count}) "
        f"POLICIES(PASS={policy_pass_count} FAIL={policy_fail_count})"
    )

    if fail_count > 0 or policy_fail_count > 0:
        raise typer.Exit(code=1)


@app.command("new")
@foundry_app.command("new")
def new(package_name: str) -> None:
    """(stub) Create a new MXM package scaffold named mxm-<package_name>."""
    console.print(f"[bold green]Scaffold would be created for[/] mxm-{package_name}")


@app.command("check")
@foundry_app.command("check")
def check(
    path: Annotated[Path, typer.Argument(help="Path to project")] = Path("."),
) -> None:
    """Check a repository against MXM package standards."""
    render_check_results(path)


if __name__ == "__main__":
    app()
