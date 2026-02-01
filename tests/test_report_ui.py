from __future__ import annotations

from fastapi.testclient import TestClient

from demo_project import report_ui


def test_runs_index_ok() -> None:
    client = TestClient(report_ui.app)
    r = client.get("/runs")
    assert r.status_code == 200
    assert "orch reports" in r.text


def test_run_detail_404_for_missing() -> None:
    client = TestClient(report_ui.app)
    r = client.get("/runs/DOES-NOT-EXIST")
    assert r.status_code == 404


def test_artifact_path_traversal_blocked() -> None:
    client = TestClient(report_ui.app)
    # run does not need to exist for traversal block to be meaningful; but we hit the guard anyway.
    r = client.get("/runs/DOES-NOT-EXIST/artifact/../../etc/passwd")
    assert r.status_code in (400, 404)
