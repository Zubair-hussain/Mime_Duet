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


