from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/ping")
def ping() -> dict:
    return {"pong": True}
