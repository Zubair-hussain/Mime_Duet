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


def extract_text(response) -> str:
    """Join the text blocks of a response."""
    return "\n".join(block.text for block in response.content if block.type == "text")


def run_tool_calls(
    response,
    inbox: list[dict],
    approve: Callable[[str, str], bool],
    out: Callable[[str], None] = print,
) -> list[dict]:
    """Run every tool_use block and return matching tool_result blocks."""
    results = []
    for block in response.content:
        if block.type == "tool_use":
            result = run_tool(block.name, block.input, inbox, approve, out=out)
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    return results


def check_in(
    client,
    settings: Settings,
    inbox: list[dict],
    approve: Callable[[str, str], bool] = ask_approval,
    out: Callable[[str], None] = print,
) -> str | None:
    """Run one check-in. Returns the brief, or None if Claude declined."""
    messages = [{"role": "user", "content": CHECK_IN_PROMPT}]
    while True:  # the agent loop
        response = client.beta.messages.create(**build_request(settings, messages))
        if response.stop_reason != "tool_use":
            break
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": run_tool_calls(response, inbox, approve, out)})
    if response.stop_reason == "refusal":
        out("Mini Duet declined this check-in.")
        return None
    brief = extract_text(response)
    out("\n--- Your brief ---\n" + brief)
    return brief
