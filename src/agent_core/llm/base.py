"""LLMProvider — the pluggable brain interface. Optional: agents can run with
no LLM at all (``model = None``)."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    def complete(self, prompt: str, **kwargs: Any) -> str: ...

    def summarize(self, content: Any, **kwargs: Any) -> str: ...
