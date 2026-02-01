from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


@dataclass(frozen=True)
class RunSummary:
    run_id: str
    feature_id: str | None
    started_ts: str | None
    ended_ts: str | None
    gate_ok: bool | None
    verify_ok: bool | None


def _parse_ledger(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"raw": line, "parse_error": True})
    return out


def _safe_join(base: Path, rel: str) -> Path:
    # Prevent path traversal: ensure resolved path stays under base.
    candidate = (base / rel).resolve()
    base_resolved = base.resolve()
    if base_resolved == candidate or base_resolved in candidate.parents:
        return candidate
    raise ValueError("Path traversal blocked")


def _summarize_run(run_dir: Path) -> RunSummary:
    ledger = _parse_ledger(run_dir / "ledger.jsonl")

    run_id = run_dir.name
    feature_id = None
    started_ts = ledger[0].get("ts") if ledger else None
    ended_ts = ledger[-1].get("ts") if ledger else None

    gate_ok = None
    verify_ok = None
    for rec in ledger:
        if rec.get("step") == "INTAKE" and rec.get("feature_id"):
            feature_id = rec.get("feature_id")
        if rec.get("step") == "VERIFY" and rec.get("ok") is True:
            verify_ok = True
        if rec.get("step") == "VERIFY" and rec.get("ok") is False and verify_ok is None:
            verify_ok = False
        if rec.get("step") == "GATE":
            gate_ok = rec.get("ok")

    return RunSummary(
        run_id=run_id,
        feature_id=feature_id,
        started_ts=started_ts,
        ended_ts=ended_ts,
        gate_ok=gate_ok,
        verify_ok=verify_ok,
    )


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = REPO_ROOT / "runs"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app = FastAPI(title="orch reports")


@app.get("/", response_class=HTMLResponse)
def home() -> RedirectResponse:
    return RedirectResponse(url="/runs")


@app.get("/runs", response_class=HTMLResponse)
def runs_index(request: Request) -> HTMLResponse:
    runs: list[RunSummary] = []
    if RUNS_DIR.exists():
        for p in RUNS_DIR.iterdir():
            if not p.is_dir():
                continue
            if not (p / "ledger.jsonl").exists():
                continue
            runs.append(_summarize_run(p))

    # newest first by run_id (timestamp suffix) or by mtime
    runs.sort(key=lambda r: r.run_id, reverse=True)

    return templates.TemplateResponse(
        request,
        "runs.html",
        {"runs": runs},
    )


@app.get("/runs/{run_id}", response_class=HTMLResponse)
def run_detail(run_id: str, request: Request) -> HTMLResponse:
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="run not found")

    ledger = _parse_ledger(run_dir / "ledger.jsonl")

    # Extract codex status parsed blocks
    codex_status = [
        rec
        for rec in ledger
        if rec.get("step") == "CODEX_STATUS" and isinstance(rec.get("parsed"), dict)
    ]

    # Build a list of artifact links (best-effort)
    artifacts: list[dict[str, str]] = []
    for rec in ledger:
        for key in ("stdout_path", "raw_path", "artifact", "report_path"):
            p = rec.get(key)
            if isinstance(p, str) and p.startswith(str(run_dir)):
                rel = str(Path(p).relative_to(run_dir))
                artifacts.append({"label": key, "rel": rel})

    # Dedupe
    seen = set()
    uniq_artifacts = []
    for a in artifacts:
        k = (a["label"], a["rel"])
        if k in seen:
            continue
        seen.add(k)
        uniq_artifacts.append(a)

    summary = _summarize_run(run_dir)

    return templates.TemplateResponse(
        request,
        "run_detail.html",
        {
            "summary": summary,
            "ledger": ledger,
            "codex_status": codex_status,
            "artifacts": uniq_artifacts,
        },
    )


@app.get("/runs/{run_id}/artifact/{rel_path:path}")
def artifact(run_id: str, rel_path: str) -> FileResponse:
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="run not found")

    try:
        p = _safe_join(run_dir, rel_path)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid path")

    if not p.exists() or not p.is_file():
        raise HTTPException(status_code=404, detail="artifact not found")

    return FileResponse(p)
