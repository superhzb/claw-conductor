# F-003: Local web UI for orch run reports

## Goal
Create a user-friendly local web UI to browse orch run reports.

## Requirements
- Implement a local web server (FastAPI) that reads run artifacts from `runs/`.
- Provide pages:
  - `GET /` → redirect to `/runs`
  - `GET /runs` → list runs (newest first)
  - `GET /runs/{run_id}` → run detail page
- Display, at minimum:
  - run_id, feature_id
  - step timeline (steps from ledger.jsonl)
  - verify status + return code
  - Codex usage summary (from parsed `/status` entries in ledger)
  - links to artifacts (plan, review, verify logs, codex status raw/parsed)
- Must be local-only, no external APIs.
- Add tests for the UI endpoints.

## Notes
- Prefer server-rendered HTML with Jinja2.
- Prevent path traversal when serving artifacts.
