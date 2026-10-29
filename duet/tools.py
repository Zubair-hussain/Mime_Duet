"""The actions Claude may ask for. Claude only asks; this code does the work."""

from __future__ import annotations

import json
from collections.abc import Callable

TOOLS = [
    {
        "name": "read_inbox",
        "description": "Return the user's unread messages as JSON.",
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        "strict": True,
    },
    {
        "name": "send_message",
        "description": "Send a message on the user's behalf. The user must approve it first.",
        "input_schema": {
            "type": "object",
            "properties": {"to": {"type": "string"}, "text": {"type": "string"}},
            "required": ["to", "text"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

DECLINED = "The user declined. Do not send this message."


def run_tool(
    name: str,
    args: dict,
    inbox: list[dict],
    approve: Callable[[str, str], bool],
    send: Callable[[str, str], None] | None = None,
    out: Callable[[str], None] = print,
) -> str:
    """Run one tool call and return the result text for Claude."""
    if name == "read_inbox":
        return json.dumps(inbox)
    if name == "send_message":
        if approve(args["to"], args["text"]):
            if send is not None:
                send(args["to"], args["text"])  # plug in your real email API here
            out("Sent.")
            return "Sent."
        return DECLINED
    return f"Unknown tool: {name}"
