from __future__ import annotations

from pathlib import Path

from orch.config import OrchSettings
from orch.runner import run_feature


def test_orch_run_f001_creates_artifacts(tmp_path: Path, monkeypatch) -> None:
    # Run inside a temp copy of the repo to avoid polluting the working tree.
    # We copy only what we need.
    import shutil

    repo_root = tmp_path / "repo"

    def _ignore(_dir, names):
        return {
            n
            for n in names
            if n in {".venv", "runs", ".pytest_cache", "__pycache__", ".git"}
        }

    shutil.copytree(Path.cwd(), repo_root, dirs_exist_ok=True, ignore=_ignore)

    monkeypatch.chdir(repo_root)

    settings = OrchSettings()
    settings.repo_root = repo_root

    run_dir = run_feature("F-001", settings)

    assert (run_dir / "ledger.jsonl").exists()
    assert (run_dir / "plan" / "plan.md").exists()
    assert (run_dir / "review" / "review.md").exists()
    assert (run_dir / "verify").exists()
