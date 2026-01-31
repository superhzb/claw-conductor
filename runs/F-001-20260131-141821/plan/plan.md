# Plan

## Overview
Add a new `/ping` endpoint returning `{"pong": true}`.

## Files to Change
- demo_project/app.py
- tests/test_integration.py
- tests/test_e2e.py

## Steps
1. Add `@app.get('/ping')` route returning JSON.
2. Add integration test with FastAPI TestClient.
3. Add e2e test that runs uvicorn and calls `/ping`.

## Tests
Run `python -m pytest`.

