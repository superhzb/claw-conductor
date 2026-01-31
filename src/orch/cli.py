from __future__ import annotations

import typer

from .config import OrchSettings
from .runner import run_feature

app = typer.Typer(add_completion=False, help="Local orchestration CLI")


@app.command()
def run(feature_id: str) -> None:
    """Run an orchestration pipeline for a feature (e.g. F-001)."""
    settings = OrchSettings()
    run_feature(feature_id, settings)


@app.command()
def version() -> None:
    """Print the orch version."""
    from . import __version__

    typer.echo(__version__)


if __name__ == "__main__":
    app()
