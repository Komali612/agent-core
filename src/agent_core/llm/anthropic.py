"""Default Claude-backed provider. Requires ``agent-core[anthropic]``.

Kept import-light: the anthropic SDK is imported lazily so agent_core stays
importable without it. The real Messages API + tool-use loop is left as a TODO
for the implementation phase (consult the claude-api reference when wiring it).
"""
from __future__ import annotations

from typing import Any

DEFAULT_MODEL = "claude-sonnet-5"


class AnthropicProvider:
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or DEFAULT_MODEL
        self._api_key = api_key
        self._client = None

    def _client_lazy(self):
        if self._client is None:
            import os

            from anthropic import Anthropic  # requires agent-core[anthropic]

            self._client = Anthropic(
                api_key=self._api_key or os.environ.get("ANTHROPIC_API_KEY")
            )
        return self._client

    def complete(self, prompt: str, **kwargs: Any) -> str:
        # TODO(impl): call the Messages API via self._client_lazy()
        raise NotImplementedError("wire up the Anthropic Messages API here")

    def summarize(self, content: Any, **kwargs: Any) -> str:
        return self.complete(f"Summarize:\n{content}")
