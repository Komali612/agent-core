from agent_core import Agent, Handler, Skill
from agent_core.manager import RunManager


class Ping(Skill):
    name = "ping"

    def run(self):
        return "pong"


class H(Handler):
    def handle(self, ctx):
        return ctx.done(ctx.skills.ping())


def test_agent_constructs_and_runs():
    agent = Agent(name="t", prompt="hi", skills=[Ping()], handler=H())
    assert RunManager(agent).run_once()["result"] == "pong"
