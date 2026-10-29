"""The agent loop: ask Claude, run its tool calls, send back the results, repeat."""

from __future__ import annotations

from collections.abc import Callable

from .approval import ask_approval
from .config import Settings
from .tools import TOOLS, run_tool

CHECK_IN_PROMPT = "Time for a check-in. What needs my attention?"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


