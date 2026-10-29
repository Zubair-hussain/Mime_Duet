"""Tests for duet.config."""

import json

import pytest

from duet.config import DEFAULT_SYSTEM, MODEL, Settings, load_settings, validate


def test_defaults_match_the_video():
    settings = Settings()
    assert settings.model == "claude-opus-5-5"
    assert settings.effort == "medium"
    assert settings.max_tokens == 16000
    assert settings.check_every_seconds == 10800
    assert settings.system == DEFAULT_SYSTEM


