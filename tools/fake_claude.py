#!/usr/bin/env python3
"""Deterministic local stand-in for Claude Code.

This script applies the F-001 change directly so `orch run F-001` works end-to-end.

Usage:
  python tools/fake_claude.py "<prompt>"
"""

from __future__ import annotations

import re
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[1]


def ensure_ping_endpoint() -> None:
    app_py = REPO / "demo_project" / "app.py"
    text = app_py.read_text(encoding="utf-8")

    if "/ping" in text:
        return

    # Add endpoint after existing /health.
    if "@app.get(\"/health\")" in text:
        text += (
            "\n\n@app.get(\"/ping\")\n"
            "def ping() -> dict:\n"
            "    return {\"pong\": True}\n"
        )
    else:
        # Fallback
        text += (
            "\n\n@app.get(\"/ping\")\n"
            "def ping() -> dict:\n"
            "    return {\"pong\": True}\n"
        )

    app_py.write_text(text, encoding="utf-8")


def ensure_tests() -> None:
    tests_dir = REPO / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    (tests_dir / "__init__.py").write_text("", encoding="utf-8")

    integration = tests_dir / "test_integration.py"
    if not integration.exists():
        integration.write_text(
            "from fastapi.testclient import TestClient\n\n"
            "from demo_project.app import app\n\n"
            "client = TestClient(app)\n\n"
            "def test_health() -> None:\n"
            "    r = client.get('/health')\n"
            "    assert r.status_code == 200\n"
            "    assert r.json() == {'ok': True}\n\n"
            "def test_ping() -> None:\n"
            "    r = client.get('/ping')\n"
            "    assert r.status_code == 200\n"
            "    assert r.json() == {'pong': True}\n",
            encoding="utf-8",
        )

    e2e = tests_dir / "test_e2e.py"
    if not e2e.exists():
        e2e.write_text(
            "import socket\n"
            "import subprocess\n"
            "import sys\n"
            "import time\n\n"
            "import httpx\n\n"
            "def _free_port() -> int:\n"
            "    with socket.socket() as s:\n"
            "        s.bind(('127.0.0.1', 0))\n"
            "        return s.getsockname()[1]\n\n"
            "def test_e2e_ping() -> None:\n"
            "    port = _free_port()\n"
            "    cmd = [sys.executable, '-m', 'uvicorn', 'demo_project.app:app', '--host', '127.0.0.1', '--port', str(port)]\n"
            "    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)\n"
            "    try:\n"
            "        # Wait briefly for server\n"
            "        deadline = time.time() + 5\n"
            "        url = f'http://127.0.0.1:{port}/ping'\n"
            "        last_err = None\n"
            "        while time.time() < deadline:\n"
            "            try:\n"
            "                r = httpx.get(url, timeout=0.5)\n"
            "                if r.status_code == 200:\n"
            "                    assert r.json() == {'pong': True}\n"
            "                    return\n"
            "            except Exception as e:  # noqa: BLE001\n"
            "                last_err = e\n"
            "                time.sleep(0.1)\n"
            "        raise AssertionError(f'e2e request never succeeded; last error: {last_err}')\n"
            "    finally:\n"
            "        p.terminate()\n"
            "        try:\n"
            "            p.wait(timeout=5)\n"
            "        except subprocess.TimeoutExpired:\n"
            "            p.kill()\n",
            encoding="utf-8",
        )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fake_claude.py <prompt>", file=sys.stderr)
        return 2

    prompt = sys.argv[1]

    # Only implement known demo features; otherwise no-op.
    if re.search(r"F-001|/ping|pong", prompt, re.IGNORECASE):
        ensure_ping_endpoint()
        ensure_tests()
        print("(fake_claude) Applied F-001 changes: /ping + tests")
        return 0

    if re.search(r"F-003|report(\s|-)ui|runs\s*/", prompt, re.IGNORECASE):
        # F-003 is implemented directly in-repo for the demo.
        print("(fake_claude) F-003 already present (report UI)")
        return 0

    if re.search(r"F-002|preset greeting|greeter", prompt, re.IGNORECASE):
        # F-002 is already implemented in this repo; keep it idempotent.
        # (In a real run, Claude Code would apply changes here.)
        print("(fake_claude) F-002 already present (greeter)")
        return 0

    print("(fake_claude) No-op")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
