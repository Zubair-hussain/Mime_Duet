"""Load the messages Mini Duet reads. Swap this for a real email API later."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_KEYS = ("from", "subject", "body")
DEFAULT_INBOX = [
    {"from": "Sara (client)", "subject": "Invoice #42?", "body": "Hi! Did you send invoice #42?"},
    {"from": "Calendar", "subject": "Dentist at 4:30 PM today", "body": ""},
]


