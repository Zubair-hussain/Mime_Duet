"""Settings for Mini Duet, with optional overrides from a JSON file."""

from __future__ import annotations

import json
from dataclasses import dataclass, fields, replace
from pathlib import Path

MODEL = "claude-opus-5-5"
DEFAULT_CONFIG_PATH = "duet.config.json"
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
DEFAULT_SYSTEM = (
    "You are Mini Duet, a proactive assistant. Read the user's inbox, "
    "write a short brief of what needs attention, and draft replies where useful. "
    "Use send_message only for replies that are clearly helpful."
)


