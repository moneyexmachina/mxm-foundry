from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(
    add_completion=False, help="MXM package scaffolding, checks, and sync."
)
console = Console()


@app.command("new")
def new(package_name: str) -> None:
    """(stub) Create a new MXM package scaffold named mxm-<package_name>."""
    console.print(f"[bold green]Scaffold would be created for[/] mxm-{package_name}")


@app.command("check")
def check() -> None:
    """(stub) Check the repo against MXM standards."""
    console.print("[bold green]OK[/] repo looks fine (placeholder).")


if __name__ == "__main__":
    app()
