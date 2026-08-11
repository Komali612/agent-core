"""The smallest agent you can write against the framework."""
from agent_core import Agent, Handler, Skill, runtime


class Hello(Skill):
    name = "hello"

    def run(self, who: str = "world"):
        return f"hello, {who}"


class HelloHandler(Handler):
    def handle(self, ctx):
        return ctx.done(ctx.skills.hello(who="agents"))


agent = Agent(
    name="minimal",
    prompt="Say hello.",
    skills=[Hello()],
    handler=HelloHandler(),
)

if __name__ == "__main__":
    runtime.run(agent)
