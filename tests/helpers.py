"""Small fakes so tests never call the real API."""

import copy
from types import SimpleNamespace


def text_block(text):
    """A text block, like the ones in a real response."""
    return SimpleNamespace(type="text", text=text)


def tool_use_block(block_id, name, tool_input=None):
    """A tool_use block: Claude asking us to run a tool."""
    return SimpleNamespace(type="tool_use", id=block_id, name=name, input=tool_input or {})


def response(stop_reason, *blocks):
    """A whole response with a stop reason and content blocks."""
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


