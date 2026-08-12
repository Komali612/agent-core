from agent_core import Agent
from agent_core.service import create_app


def test_service_exposes_health_routes():
    app = create_app(Agent(name="t", prompt="x"))
    paths = {route.path for route in app.routes}
    assert "/healthz" in paths
    assert "/readyz" in paths
    assert "/run" in paths
