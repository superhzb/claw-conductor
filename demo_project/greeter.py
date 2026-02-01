from __future__ import annotations

import sys
import typer

app = typer.Typer(add_completion=False)


@app.command()
def main(text: str = typer.Argument(..., help="Any text; it will be ignored")) -> None:
    """Echo a preset greeting regardless of input."""
    _ = text
    typer.echo("Hello from orch!")


def _entry() -> None:
    # Allow `python -m demo_project.greeter <text>` style usage.
    app()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # show help
        app(["--help"])
    else:
        _entry()
