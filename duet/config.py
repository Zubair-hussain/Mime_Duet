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


@dataclass(frozen=True)
class Settings:
    """Everything you can change without touching the code."""

    model: str = MODEL
    effort: str = "medium"
    max_tokens: int = 16000
    check_every_seconds: int = 3 * 60 * 60
    inbox_path: str = "data/inbox.json"
    system: str = DEFAULT_SYSTEM


def validate(settings: Settings) -> Settings:
    """Raise ValueError if a setting is unusable, otherwise return it unchanged."""
    for name in ("model", "effort", "inbox_path", "system"):
        value = getattr(settings, name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
    for name in ("check_every_seconds", "max_tokens"):
        value = getattr(settings, name)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be a positive whole number")
    if settings.effort not in EFFORT_LEVELS:
        raise ValueError(f"effort must be one of: {', '.join(EFFORT_LEVELS)}")
    return settings


