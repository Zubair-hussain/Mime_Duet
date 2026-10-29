"""Tests for duet.approval."""

import pytest

from duet.approval import ask_approval, format_draft


def test_draft_shows_the_recipient_and_the_text():
    draft = format_draft("Sara", "Hi there")
    assert "Sara" in draft
    assert "Hi there" in draft


