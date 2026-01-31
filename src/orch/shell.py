from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .allowlist import CommandAllowlist


@dataclass
class ShellResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


def run_allowed(
    command: str,
    *,
    cwd: Path,
    allowlist: CommandAllowlist,
    env: dict[str, str] | None = None,
    timeout_s: int | None = None,
) -> ShellResult:
    allowlist.check(command)

    p = subprocess.run(
        command,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        env=env,
        timeout=timeout_s,
    )
    return ShellResult(
        command=command,
        returncode=p.returncode,
        stdout=p.stdout,
        stderr=p.stderr,
    )
