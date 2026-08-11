"""A tiny registry, used by discovery-style setups. Option B doesn't need it
(skills are listed explicitly in ``skills.py``), but it's here for tooling and
tests."""
from __future__ import annotations

from .base import Skill


class SkillRegistry:
    def __init__(self) -> None:
        self._by_name: dict[str, Skill] = {}

    def add(self, skill: Skill) -> None:
        self._by_name[skill.name] = skill

    def get(self, name: str) -> Skill:
        return self._by_name[name]

    def all(self) -> list[Skill]:
        return list(self._by_name.values())
