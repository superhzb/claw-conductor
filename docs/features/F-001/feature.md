# F-001: Add `GET /ping` endpoint

## Goal
Add a simple health-ish endpoint so external monitors can verify the service is alive.

## Requirements
- Add `GET /ping` that returns JSON: `{ "pong": true }`
- Add/extend tests so both integration and e2e tests pass
- Keep existing `/health` endpoint working

## Notes
This repo contains a demo FastAPI app under `demo_project/`.

