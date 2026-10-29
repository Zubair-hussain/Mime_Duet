"""Load the messages Mini Duet reads. Swap this for a real email API later."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_KEYS = ("from", "subject", "body")
DEFAULT_INBOX = [
    {"from": "Sara (client)", "subject": "Invoice #42?", "body": "Hi! Did you send invoice #42?"},
    {"from": "Calendar", "subject": "Dentist at 4:30 PM today", "body": ""},
]


def validate_inbox(items: object) -> list[dict]:
    """Check the inbox shape and return it unchanged, or raise ValueError."""
    if not isinstance(items, list):
        raise ValueError("Inbox must be a JSON list of messages")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Message {index} must be an object")
        missing = [key for key in REQUIRED_KEYS if key not in item]
        if missing:
            raise ValueError(f"Message {index} is missing: {', '.join(missing)}")
    return items


def load_inbox(path: str | Path | None = None) -> list[dict]:
    """Read the inbox from a JSON file, or use the demo inbox if the file is absent."""
    if path is None or not Path(path).exists():
        return list(DEFAULT_INBOX)
    try:
        items = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise ValueError(f"Inbox file is not valid JSON: {path}") from err
    return validate_inbox(items)
