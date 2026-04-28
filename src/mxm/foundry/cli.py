from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from mxm.foundry.checks.runner import run_checks

app = typer.Typer(
    add_completion=False,
    help="MXM package scaffolding, checks, and sync.",
)

foundry_app = typer.Typer(
    add_completion=False,
    help="Package scaffolding and checks.",
)

console = Console()


def render_check_results(path: Path) -> None:
    project_root = path.resolve()

    if not project_root.exists():
        console.print(f"[bold red]Error:[/] Path does not exist: {project_root}")
        raise typer.Exit(code=1)

    results = run_checks(project_root)

    table = Table(title=f"MXM Foundry Check: {project_root}")
    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Status")
    table.add_column("Check")
    table.add_column("Message")

    fail_count = 0

    for result in results:
        if result.status == "pass":
            status = "[green]PASS[/]"
        elif result.status == "warn":
            status = "[yellow]WARN[/]"
        else:
            status = "[red]FAIL[/]"
            fail_count += 1

        table.add_row(result.code, status, result.name, result.message)

    console.print(table)

    pass_count = sum(result.status == "pass" for result in results)
    warn_count = sum(result.status == "warn" for result in results)

    console.print(f"\nSummary: PASS={pass_count} WARN={warn_count} FAIL={fail_count}")

    if fail_count > 0:
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
