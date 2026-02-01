from __future__ import annotations

import subprocess
import sys


def test_greeter_cli_prints_preset_greeting() -> None:
    p = subprocess.run(
        [sys.executable, "-m", "demo_project.greeter", "anything"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert p.returncode == 0
    assert p.stdout.strip() == "Hello from orch!"
