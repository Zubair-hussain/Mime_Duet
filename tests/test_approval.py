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


def test_the_draft_is_shown_before_asking():
    shown = []
    ask_approval("Sara", "Hi", input_fn=lambda prompt: "n", out=shown.append)
    assert "Sara" in shown[0]


def test_the_prompt_text_is_stable():
    prompts = []
    ask_approval(
        "Sara", "Hi", input_fn=lambda prompt: prompts.append(prompt) or "y", out=lambda text: None
    )
    assert prompts == ["Approve? (y/n) "]


def test_it_uses_the_real_input_and_print_by_default(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert ask_approval("Sara", "Hi") is True
    assert "Sara" in capsys.readouterr().out
