"""Human in the loop: nothing is sent until you type y."""

from __future__ import annotations

from collections.abc import Callable


def format_draft(to: str, text: str) -> str:
    """The message shown to you before anything is sent."""
    return f"\nMini Duet wants to send to {to}:\n  {text}"


