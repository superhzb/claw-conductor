# F-002: Demo CLI greeter

## Goal
Create a small CLI tool to use as a test project for the orch workflow.

## Requirements
- Create a CLI program `greeter`.
- When the user runs it and inputs *anything*, it replies with a **preset greeting**.
  - Example:
    - Input: `abc`
    - Output: `Hello from orch!`
- Include tests.
- Must run locally, no APIs.

## Notes
- Keep it simple and deterministic.
- Prefer Typer for the CLI.
