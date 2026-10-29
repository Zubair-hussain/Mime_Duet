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


def test_missing_default_file_gives_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_settings() == Settings()


