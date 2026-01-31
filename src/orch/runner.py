from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from rich.console import Console

from .allowlist import CommandAllowlist
from .codex_status import parse_codex_status
from .config import OrchSettings
from .ledger import Ledger
from .shell import run_allowed
from .tools import run_tool
from .types import Step


@dataclass
class RunContext:
    settings: OrchSettings
    feature_id: str
    run_id: str
    run_dir: Path
    ledger: Ledger
    console: Console

    @property
    def feature_dir(self) -> Path:
        return self.settings.repo_root / self.settings.features_dir / self.feature_id

    @property
    def demo_root(self) -> Path:
        return self.settings.repo_root


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _new_run_id(feature_id: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{feature_id}-{ts}"


def run_feature(feature_id: str, settings: OrchSettings) -> Path:
    console = Console()

    run_id = _new_run_id(feature_id)
    run_dir = settings.repo_root / settings.runs_dir / run_id
    ledger = Ledger(run_dir / "ledger.jsonl")

    ctx = RunContext(
        settings=settings,
        feature_id=feature_id,
        run_id=run_id,
        run_dir=run_dir,
        ledger=ledger,
        console=console,
    )

    run_dir.mkdir(parents=True, exist_ok=True)

    ctx.ledger.append(
        {
            "step": Step.INTAKE,
            "feature_id": feature_id,
            "run_id": run_id,
        }
    )

    _step_intake(ctx)
    _step_plan(ctx)
    _step_execute(ctx)

    ok = _step_verify(ctx)
    if not ok:
        _step_fixloop(ctx)

    _step_review(ctx)
    _step_gate(ctx)
    _step_publish(ctx)

    console.print(f"Run complete: {run_dir}")
    return run_dir


def _step_intake(ctx: RunContext) -> None:
    feature_md = ctx.feature_dir / "feature.md"
    if not feature_md.exists():
        raise FileNotFoundError(f"Missing feature doc: {feature_md}")

    intake = _read(feature_md)
    _write(ctx.run_dir / "intake" / "feature.md", intake)

    ctx.ledger.append(
        {
            "step": Step.INTAKE,
            "artifact": str(ctx.run_dir / "intake" / "feature.md"),
        }
    )


def _codex_status_capture(ctx: RunContext, label: str) -> dict:
    usage_dir = ctx.run_dir / "usage"
    usage_dir.mkdir(parents=True, exist_ok=True)

    res = run_tool(ctx.settings.codex_cmd, prompt="/status", cwd=ctx.settings.repo_root)
    raw_path = usage_dir / f"codex-status-{label}.txt"
    _write(raw_path, res.stdout + ("\n" + res.stderr if res.stderr else ""))

    parsed = parse_codex_status(res.stdout)
    parsed_path = usage_dir / f"codex-status-{label}.json"
    _write(parsed_path, json.dumps(parsed.as_dict(), indent=2))

    ctx.ledger.append(
        {
            "step": "CODEX_STATUS",
            "label": label,
            "returncode": res.returncode,
            "raw_path": str(raw_path),
            "parsed": parsed.as_dict(),
        }
    )

    return {"raw_path": str(raw_path), "parsed": parsed.as_dict()}


def _step_plan(ctx: RunContext) -> None:
    _codex_status_capture(ctx, "pre-plan")

    feature_md = _read(ctx.feature_dir / "feature.md")
    prompt = (
        "You are Codex (PLAN). Produce a concrete implementation plan for the feature below. "
        "Return markdown with sections: Overview, Files to Change, Steps, Tests.\n\n"
        + feature_md
    )

    res = run_tool(ctx.settings.codex_cmd, prompt=prompt, cwd=ctx.settings.repo_root)
    out_path = ctx.run_dir / "plan" / "plan.md"
    _write(out_path, res.stdout)

    ctx.ledger.append(
        {
            "step": Step.PLAN,
            "tool": "codex",
            "returncode": res.returncode,
            "stdout_path": str(out_path),
            "stderr": res.stderr,
        }
    )

    _codex_status_capture(ctx, "post-plan")


def _step_execute(ctx: RunContext) -> None:
    plan = _read(ctx.run_dir / "plan" / "plan.md")
    feature = _read(ctx.feature_dir / "feature.md")

    prompt = (
        "You are Claude Code (EXECUTE). Implement the feature in this repo. "
        "Follow the plan. Make code changes in-place. After changes, do not run arbitrary commands. "
        "\n\nPLAN:\n" + plan + "\n\nFEATURE:\n" + feature
    )

    res = run_tool(ctx.settings.claude_cmd, prompt=prompt, cwd=ctx.settings.repo_root)
    out_path = ctx.run_dir / "execute" / "claude-output.txt"
    _write(out_path, res.stdout)

    ctx.ledger.append(
        {
            "step": Step.EXECUTE,
            "tool": "claude",
            "returncode": res.returncode,
            "stdout_path": str(out_path),
            "stderr": res.stderr,
            "tokens": None,
        }
    )


def _step_verify(ctx: RunContext) -> bool:
    allowlist = CommandAllowlist.from_regexes(ctx.settings.allowlist_regex)

    cmd = ctx.settings.verify_command
    res = run_allowed(cmd, cwd=ctx.settings.repo_root, allowlist=allowlist)

    out_path = ctx.run_dir / "verify" / "pytest.txt"
    _write(out_path, res.stdout + ("\n" + res.stderr if res.stderr else ""))

    ok = res.returncode == 0
    ctx.ledger.append(
        {
            "step": Step.VERIFY,
            "command": cmd,
            "returncode": res.returncode,
            "stdout_path": str(out_path),
            "ok": ok,
        }
    )
    return ok


def _step_fixloop(ctx: RunContext) -> None:
    allowlist = CommandAllowlist.from_regexes(ctx.settings.allowlist_regex)

    for i in range(1, ctx.settings.max_fix_iterations + 1):
        ctx.ledger.append({"step": Step.FIXLOOP, "iteration": i})

        last = _read(ctx.run_dir / "verify" / "pytest.txt")
        prompt = (
            "You are Claude Code (FIX). Tests are failing. Fix the repo code until tests pass. "
            "Here is the failing output:\n\n" + last
        )

        res = run_tool(ctx.settings.claude_cmd, prompt=prompt, cwd=ctx.settings.repo_root)
        out_path = ctx.run_dir / "fix" / f"claude-fix-{i}.txt"
        _write(out_path, res.stdout)

        ctx.ledger.append(
            {
                "step": "FIX",
                "tool": "claude",
                "iteration": i,
                "returncode": res.returncode,
                "stdout_path": str(out_path),
                "stderr": res.stderr,
                "tokens": None,
            }
        )

        # Re-run tests
        res2 = run_allowed(ctx.settings.verify_command, cwd=ctx.settings.repo_root, allowlist=allowlist)
        out_path2 = ctx.run_dir / "verify" / f"pytest-fix-{i}.txt"
        _write(out_path2, res2.stdout + ("\n" + res2.stderr if res2.stderr else ""))

        ok = res2.returncode == 0
        ctx.ledger.append(
            {
                "step": Step.VERIFY,
                "after_fix_iteration": i,
                "returncode": res2.returncode,
                "stdout_path": str(out_path2),
                "ok": ok,
            }
        )

        if ok:
            return

    raise RuntimeError("Fix loop exhausted; tests still failing")


def _step_review(ctx: RunContext) -> None:
    _codex_status_capture(ctx, "pre-review")

    plan = _read(ctx.run_dir / "plan" / "plan.md")
    prompt = (
        "You are Codex (REVIEW). Review the final repo changes against the plan. "
        "Output markdown: Summary, Potential Issues, Test Coverage, Next Steps.\n\n"
        "PLAN:\n" + plan
    )

    res = run_tool(ctx.settings.codex_cmd, prompt=prompt, cwd=ctx.settings.repo_root)
    out_path = ctx.run_dir / "review" / "review.md"
    _write(out_path, res.stdout)

    ctx.ledger.append(
        {
            "step": Step.REVIEW,
            "tool": "codex",
            "returncode": res.returncode,
            "stdout_path": str(out_path),
            "stderr": res.stderr,
        }
    )

    _codex_status_capture(ctx, "post-review")


def _step_gate(ctx: RunContext) -> None:
    # Gate: ensure verify passed at least once.
    ledger_text = (ctx.run_dir / "ledger.jsonl").read_text(encoding="utf-8")
    ok = '"step": "VERIFY"' in ledger_text and '"ok": true' in ledger_text

    ctx.ledger.append({"step": Step.GATE, "ok": ok})

    if not ok:
        raise RuntimeError("GATE failed: no passing VERIFY recorded")


def _step_publish(ctx: RunContext) -> None:
    # Publish: create a simple run report.
    report = {
        "feature_id": ctx.feature_id,
        "run_id": ctx.run_id,
        "run_dir": str(ctx.run_dir),
        "published": True,
        "env": {
            "ORCH_CODEX_CMD": os.environ.get("ORCH_CODEX_CMD"),
            "ORCH_CLAUDE_CMD": os.environ.get("ORCH_CLAUDE_CMD"),
        },
    }

    out_path = ctx.run_dir / "publish" / "report.json"
    _write(out_path, json.dumps(report, indent=2))

    ctx.ledger.append({"step": Step.PUBLISH, "report_path": str(out_path)})
