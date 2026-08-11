"""agent_core — the shared framework every agent is built on.

Agents never copy this code; they depend on it as a versioned package
(``agent-core==x.y``). Change something here, tag a release, and every agent
picks it up on its next version bump. That is what keeps every agent identical.
"""
from __future__ import annotations

from . import runtime
from .agent import Agent
from .handler import Handler
from .skills import Skill

__version__ = "0.1.0"
__all__ = ["Agent", "Handler", "Skill", "runtime", "__version__"]
