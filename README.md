# orch

`orch` is a local-only orchestration CLI that runs **terminal tools** (no APIs):

- **Codex** for **PLAN** and **REVIEW**
- **Claude Code** for **EXECUTE** and **FIX**

It maintains a run folder (`runs/<run_id>/`) with logs and a `ledger.jsonl` of every step.

## Quickstart (demo)

This repo includes deterministic local stand-ins for Codex/Claude so the demo can run end-to-end without external dependencies.

```bash
# from repo root
python -m venv .venv && source .venv/bin/activate
pip install -e .

orch run F-001
```

Run artifacts are written to `runs/`.

## Real tools

Set env vars to point `orch` at real tools:

- `ORCH_CODEX_CMD="codex"`
- `ORCH_CLAUDE_CMD="claude"`

By default, the demo uses `python tools/fake_codex.py` and `python tools/fake_claude.py`.
