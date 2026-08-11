"""A keyless provider so a freshly stamped agent runs with no API key."""
from __future__ import annotations

from typing import Any


class NoOpProvider:
    """Echoes instead of calling a model. Handy for local runs and tests."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return f"[noop-llm] {prompt[:200]}"

    def summarize(self, content: Any, **kwargs: Any) -> str:
        return f"[noop-llm summary of {len(str(content))} chars]"
