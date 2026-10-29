"""Tests for duet.approval."""

import pytest

from duet.approval import ask_approval, format_draft


def test_draft_shows_the_recipient_and_the_text():
    draft = format_draft("Sara", "Hi there")
    assert "Sara" in draft
    assert "Hi there" in draft


@pytest.mark.parametrize("answer", ["y", "Y", " y ", "\ty\n"])
def test_y_approves(answer):
    assert ask_approval("Sara", "Hi", input_fn=lambda prompt: answer, out=lambda text: None) is True


@pytest.mark.parametrize("answer", ["n", "", "yes", "maybe"])
def test_anything_else_declines(answer):
    assert (
        ask_approval("Sara", "Hi", input_fn=lambda prompt: answer, out=lambda text: None) is False
    )


