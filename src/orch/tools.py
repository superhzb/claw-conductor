from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


def run_tool(
    cmd: str,
    *,
    prompt: str,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_s: int | None = None,
) -> ToolResult:
    """Run a local terminal tool (Codex/Claude) via shell.

    `cmd` is the base command; we append the prompt as a single POSIX-shell-escaped argument.

    Notes:
    - Use env vars ORCH_CODEX_CMD / ORCH_CLAUDE_CMD to point at real tools.
    - Prompts may include newlines; we must escape safely.
    """

    full = f"{cmd} {shlex.quote(prompt)}"
    p = subprocess.run(
        full,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        env=env,
        timeout=timeout_s,
    )
    return ToolResult(full, p.returncode, p.stdout, p.stderr)
