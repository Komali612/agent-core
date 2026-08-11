"""RunManager — orchestrates a single run: build context, invoke the handler,
capture the result, emit metrics."""
from __future__ import annotations

from . import monitoring
from .context import RunContext
from .llm import get_llm
from .logging import get_logger

log = get_logger("agent.manager")


class RunManager:
    def __init__(self, agent) -> None:
        self.agent = agent
        self.llm = get_llm(agent.model)

    def run_once(self, payload: dict | None = None):
        monitoring.runs_started.inc()
        ctx = RunContext(self.agent, payload=payload, llm=self.llm)
        if self.agent.handler is None:
            raise RuntimeError("agent has no handler")
        try:
            result = self.agent.handler.handle(ctx)
            monitoring.runs_ok.inc()
            log.info("run complete: %s", self.agent.name)
            return result
        except Exception:
            monitoring.runs_failed.inc()
            log.exception("run failed: %s", self.agent.name)
            raise
