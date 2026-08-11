"""FastAPI app factory for ``serve`` mode + a uvicorn entrypoint.

Heavy deps (fastapi/uvicorn) are imported lazily so ``import agent_core`` works
without them; they're only needed when an agent actually runs in serve mode.
"""
from __future__ import annotations

from . import monitoring
from .intake import Intake
from .manager import RunManager


def create_app(agent):
    from fastapi import FastAPI, Request

    app = FastAPI(title=agent.name)
    manager = RunManager(agent)
    intake = Intake()

    @app.get("/healthz")
    def healthz():
        return monitoring.healthz()

    @app.get("/readyz")
    def readyz():
        return {"status": "ready", "agent": agent.name}

    @app.get("/metrics")
    def metrics():
        return monitoring.metrics()

    @app.post("/run")
    async def run(request: Request):
        payload = intake.accept(await request.json())
        return manager.run_once(payload)

    return app


def serve(agent, host: str = "0.0.0.0", port: int = 8080) -> None:
    import uvicorn

    uvicorn.run(create_app(agent), host=host, port=port)
