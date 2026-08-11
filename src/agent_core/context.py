"""RunContext — what a Handler receives for a single run.

Gives the handler ergonomic access to the agent's skills
(``ctx.skills.<name>()``), the optional LLM (``ctx.llm``), and a ``done()``
helper to return a result.
"""
from __future__ import annotations

from typing import Any


class SkillProxy:
    """Lets a handler call skills by name: ``ctx.skills.fetch_issues(...)``."""

    def __init__(self, skills: dict[str, Any]):
        self._skills = skills

    def __getattr__(self, name: str):
        try:
            skill = self._skills[name]
        except KeyError as exc:
            raise AttributeError(f"no skill named {name!r}") from exc
        return skill.run


class RunContext:
    def __init__(self, agent, payload: dict | None = None, llm=None):
        self.agent = agent
        self.payload = payload or {}
        self.skills = SkillProxy(agent.skill_map())
        self.llm = llm

    def done(self, result: Any = None) -> dict:
        return {"agent": self.agent.name, "result": result}
