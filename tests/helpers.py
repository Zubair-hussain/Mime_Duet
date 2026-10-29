"""Small fakes so tests never call the real API."""

import copy
from types import SimpleNamespace


def text_block(text):
    """A text block, like the ones in a real response."""
    return SimpleNamespace(type="text", text=text)


