#!/usr/bin/env python3
"""Deterministic local stand-in for Codex CLI.

Usage:
  python tools/fake_codex.py "<prompt>"

Special:
  If prompt is exactly `/status`, prints a status block that orch can parse.
"""

from __future__ import annotations

import hashlib
import sys
import time


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fake_codex.py <prompt>", file=sys.stderr)
        return 2

    prompt = sys.argv[1]

    if prompt.strip() == "/status":
        # Fake-but-parseable status output.
        # Make tokens deterministic based on cwd+time bucket.
        import os

        seed = os.getcwd().encode("utf-8")
        h = hashlib.sha256(seed + str(int(time.time()) // 60).encode("utf-8")).hexdigest()
        in_tok = int(h[:4], 16) % 2000 + 100
        out_tok = int(h[4:8], 16) % 1000 + 50
        total = in_tok + out_tok
        cost = round(total * 0.000002, 6)
        print("Model: gpt-5.2-codex")
        print(f"Input tokens: {in_tok}")
        print(f"Output tokens: {out_tok}")
        print(f"Total tokens: {total}")
        print(f"Cost (USD): ${cost}")
        print("Elapsed: 0.2s")
        return 0

    lower = prompt.lower()
    if "(plan)" in lower or "implementation plan" in lower:
        if "f-003" in lower or ("frontend" in lower and "report" in lower):
            print(
                "# Plan\n\n"
                "## Overview\n"
                "Add a local FastAPI + Jinja2 UI to browse orch run reports in `runs/`.\n\n"
                "## Files to Change\n"
                "- pyproject.toml (add jinja2 dep + console script)\n"
                "- demo_project/report_ui.py\n"
                "- demo_project/templates/runs.html\n"
                "- demo_project/templates/run_detail.html\n"
                "- tests/test_report_ui.py\n\n"
                "## Steps\n"
                "1. Implement `/runs` and `/runs/{run_id}` server-rendered pages.\n"
                "2. Implement artifact serving with path traversal protection.\n"
                "3. Add tests with FastAPI TestClient.\n\n"
                "## Tests\n"
                "Run `python -m pytest -q`.\n"
            )
            return 0

        if "f-002" in lower or "preset greeting" in lower or "greeter" in lower:
            print(
                "# Plan\n\n"
                "## Overview\n"
                "Add a simple Typer-based CLI `greeter` that prints a preset greeting regardless of input.\n\n"
                "## Files to Change\n"
                "- pyproject.toml (add console script)\n"
                "- demo_project/greeter.py\n"
                "- tests/test_greeter_cli.py\n\n"
                "## Steps\n"
                "1. Implement Typer CLI with one argument and constant output.\n"
                "2. Add a test invoking the module and asserting output.\n"
                "3. Run `python -m pytest -q`.\n\n"
                "## Tests\n"
                "Run `python -m pytest -q`.\n"
            )
            return 0

        print(
            "# Plan\n\n"
            "## Overview\n"
            "Add a new `/ping` endpoint returning `{\"pong\": true}`.\n\n"
            "## Files to Change\n"
            "- demo_project/app.py\n"
            "- tests/test_integration.py\n"
            "- tests/test_e2e.py\n\n"
            "## Steps\n"
            "1. Add `@app.get('/ping')` route returning JSON.\n"
            "2. Add integration test with FastAPI TestClient.\n"
            "3. Add e2e test that runs uvicorn and calls `/ping`.\n\n"
            "## Tests\n"
            "Run `python -m pytest -q`.\n"
        )
        return 0

    if "(review)" in lower or "review the final" in lower:
        if "f-003" in lower or "report" in lower and "runs" in lower:
            print(
                "# Review\n\n"
                "## Summary\n"
                "Local FastAPI + Jinja2 report UI added to browse `runs/` and inspect ledger/artifacts.\n\n"
                "## Potential Issues\n"
                "Ensure artifact serving blocks path traversal (should resolve under run_dir).\n\n"
                "## Test Coverage\n"
                "Includes TestClient coverage for routes and traversal handling.\n\n"
                "## Next Steps\n"
                "Add filtering/search and a nicer timeline visualization.\n"
            )
            return 0

        print(
            "# Review\n\n"
            "## Summary\n"
            "`/ping` was added and covered by integration + e2e tests.\n\n"
            "## Potential Issues\n"
            "None obvious for the demo.\n\n"
            "## Test Coverage\n"
            "Integration uses TestClient; e2e runs uvicorn and hits real HTTP.\n\n"
            "## Next Steps\n"
            "Consider adding auth / rate limiting if exposed publicly.\n"
        )
        return 0

    print("(fake_codex) No-op prompt received.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
