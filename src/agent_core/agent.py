"""The Agent object — the single assembly point every agent repo wires up.

``agent.py`` inside each agent repo is frozen and identical; it just calls
``Agent(...)`` with the four things that vary: name, prompt, skills, handler.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .handler import Handler
    from .skills import Skill


@dataclass
class Agent:
    name: str
    prompt: str
    skills: list["Skill"] = field(default_factory=list)
    handler: "Handler | None" = None
    model: str | None = None            # LLM model id, or None for no brain

    def skill_map(self) -> dict[str, "Skill"]:
        return {s.name: s for s in self.skills}
