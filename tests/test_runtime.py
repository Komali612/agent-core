from agent_core import Agent, Handler
from agent_core.service import create_app


class H(Handler):
    def handle(self, ctx):
        return ctx.done("ok")


def test_service_exposes_health_routes():
    app = create_app(Agent(name="t", prompt="x", handler=H()))
    paths = {route.path for route in app.routes}
    assert "/healthz" in paths
    assert "/readyz" in paths
    assert "/run" in paths
