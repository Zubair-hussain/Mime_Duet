"""The agent loop: ask Claude, run its tool calls, send back the results, repeat."""

from __future__ import annotations

from collections.abc import Callable

from .approval import ask_approval
from .config import Settings
from .tools import TOOLS, run_tool

CHECK_IN_PROMPT = "Time for a check-in. What needs my attention?"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def build_request(settings: Settings, messages: list[dict]) -> dict:
    """Everything we send to the API for one turn."""
    return {
        "model": settings.model,
        "max_tokens": settings.max_tokens,
        "system": settings.system,
        "tools": TOOLS,
        "messages": messages,
        "output_config": {"effort": settings.effort},
        "betas": [FALLBACK_BETA],
        "fallbacks": "default",  # safety net: retry on a backup model if a request is declined
    }


