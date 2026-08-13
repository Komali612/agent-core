from fastapi.testclient import TestClient

from agent_core import Agent, Handler
from agent_core.service import create_app


def test_service_exposes_health_routes():
    app = create_app(Agent(name="t", prompt="x"))
    paths = {route.path for route in app.routes}
    assert "/healthz" in paths
    assert "/readyz" in paths
    assert "/run" in paths


def test_run_accepts_structured_input():
    """Regression: /run must accept a *structured* (dict) `input`, not only text.

    Handler agents (e.g. the CI workers) receive a serialized object as `input`;
    an over-strict `input: str` schema rejected them with HTTP 422.
    """

    class EchoHandler(Handler):
        def handle(self, ctx):
            return ctx.done(ctx.payload.get("input"))

    client = TestClient(create_app(Agent(name="t", prompt="x", handler=EchoHandler())))
    resp = client.post("/run", json={"input": {"repo": "acme/widget", "n": 1}})
    assert resp.status_code == 200
    assert resp.json()["result"] == {"repo": "acme/widget", "n": 1}
