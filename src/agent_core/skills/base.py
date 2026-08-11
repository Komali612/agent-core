"""Skill — a single capability an agent can use.

Each agent repo lists its skills in ``skills/skills.py`` as ``SKILLS = [...]``.
"""
from __future__ import annotations

from typing import Any


class Skill:
    #: unique name; how the handler references it (``ctx.skills.<name>``)
    name: str = ""

    def run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Implement run() in your Skill subclass")
