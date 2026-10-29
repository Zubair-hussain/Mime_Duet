"""Human in the loop: nothing is sent until you type y."""

from __future__ import annotations

from collections.abc import Callable


def format_draft(to: str, text: str) -> str:
    """The message shown to you before anything is sent."""
    return f"\nMini Duet wants to send to {to}:\n  {text}"


def ask_approval(
    to: str,
    text: str,
    input_fn: Callable[[str], str] | None = None,
    out: Callable[[str], None] = print,
) -> bool:
    """Show the draft and return True only if you type y."""
    out(format_draft(to, text))
    ask = input_fn or input  # looked up now, so it can be swapped out in tests
    return ask("Approve? (y/n) ").strip().lower() == "y"
