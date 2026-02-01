from __future__ import annotations

from pathlib import Path
import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OrchSettings(BaseSettings):
    """Configuration for orch.

    Note: defaults are demo-friendly and rely on local deterministic fake tools.
    """

    model_config = SettingsConfigDict(env_prefix="ORCH_", extra="ignore")

    repo_root: Path = Field(default_factory=lambda: Path.cwd())

    # Tool commands (strings executed via the shell).
    # Use sys.executable to avoid relying on PATH/venv activation.
    codex_cmd: str = Field(default_factory=lambda: f"{sys.executable} tools/fake_codex.py")
    claude_cmd: str = Field(default_factory=lambda: f"{sys.executable} tools/fake_claude.py")

    # Where we store feature docs + run artifacts (relative to repo_root).
    docs_dir: Path = Path("docs")
    features_dir: Path = Path("docs/features")
    runs_dir: Path = Path("runs")

    # Fix loop
    max_fix_iterations: int = 3

    # Verification command (must be allowlisted)
    verify_command: str = Field(
        default_factory=lambda: (
            f"{sys.executable} -m pytest -q "
            "tests/test_integration.py tests/test_e2e.py tests/test_greeter_cli.py"
        )
    )

    # Shell command allowlist (regexes)
    allowlist_regex: tuple[str, ...] = (
        r"^python(3)?(\s|$)",
        r"^.*/python(3(\.\d+)*)?(\s|$)",
        r"^pytest(\s|$)",
        r"^.*/pytest(\s|$)",
        r"^uv(\s|$)",
        r"^pip(\s|$)",
        r"^git(\s|$)",
    )
