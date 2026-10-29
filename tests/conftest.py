"""Shared test setup: no real API calls and no real key needed."""

import os

import pytest

from duet.config import Settings

# mini_duet.py builds its client when it is imported, so a key must exist.
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-real")


@pytest.fixture
def settings():
    """Default settings."""
    return Settings()


@pytest.fixture
def inbox():
    """A one-message inbox."""
    return [{"from": "Sara", "subject": "Invoice #42?", "body": "Did you send it?"}]
